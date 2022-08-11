import asyncio
import zlib
from logging import getLogger
from ..status_code import HTTPCodes
from ..exceptions import (
    DiscordServerError5xx,
    NotFound404,
    Forbidden403,
    DiscordAPIError,
)
from typing import Union, Dict, Any
from importlib.util import find_spec
from aiohttp import ClientWebSocketResponse, ClientSession

logger = getLogger(__name__)

_ORJSON = find_spec("orjson")


if _ORJSON:
    import orjson as json

else:
    import json


class _FakeTask:
    def cancel(self):
        return True


class UnknownBucket:
    def __init__(self):
        self.lock = asyncio.Lock()
        self.close_task: _FakeTask = _FakeTask()


class Bucket(UnknownBucket):
    def __init__(self, *, discord_hash: str):
        super().__init__()
        self.bucket_hash = discord_hash

    def __eq__(self, other):
        return self.bucket_hash == other.bucket_hash


class DiscordWSMessage:
    def __init__(self, *, data, type, extra):
        self.data = data
        self.type = type
        self.extra = extra

    def json(self) -> Any:
        return json.loads(self.data)


class DiscordGatewayWebsocket(ClientWebSocketResponse):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.buffer: bytearray = bytearray()
        self.inflator = zlib.decompressobj()

    async def receive(self, *args, **kwargs):
        ws_message = await super().receive(*args, **kwargs)
        message = ws_message.data

        if isinstance(message, bytes):

            self.buffer.extend(message)

            if len(message) < 4 or message[-4:] != b"\x00\x00\xff\xff":
                return

            message = self.inflator.decompress(self.buffer)

            message = message.decode("utf-8")
            self.buffer: bytearray = bytearray()

        return DiscordWSMessage(
            data=message, type=ws_message.type, extra=ws_message.extra
        )

    async def __anext__(self) -> dict:
        return await super().__anext__()


class HTTPClient(ClientSession):
    def __init__(self, *args, **kwargs):
        self.base_uri: str = kwargs.pop(
            "discord_endpoint", "https://discord.com/api/v10"
        )
        super().__init__(
            *args,
            **kwargs,
            json_serialize=lambda x, *__, **___: json.dumps(x).decode()
            if _ORJSON
            else json.dumps(x),
            ws_response_class=DiscordGatewayWebsocket,
        )
        self.global_ratelimit: asyncio.Event = asyncio.Event()
        self.global_ratelimit.set()
        self.buckets: Dict[str, Bucket] = {}

    async def request(
        self,
        method,
        url,
        *args,
        attempt: int = 1,
        to_discord=True,
        guild_id: Union[str, int] = 0,
        channel_id: Union[int, str] = 0,
        **kwargs,
    ):

        if attempt > 5:
            logger.critical(f"Failed a {method} {url} 5 times.")
            return  # Just quit the request

        if url.startswith("ws") or not to_discord:
            return await super().request(method, url, *args, **kwargs)
        if url.startswith("/"):
            url = url[1:]

        if url.endswith("/"):
            url = url[: len(url) - 1]

        url = f"{self.base_uri}/{url}"

        await self.global_ratelimit.wait()

        bucket_hash = f"{guild_id}:{channel_id}:{url}"
        bucket = self.buckets.get(bucket_hash)

        if not bucket:
            bucket = UnknownBucket()

        await bucket.lock.acquire()

        res = await super().request(method, url, *args, **kwargs)

        await self.log_request(res)

        if isinstance(bucket, UnknownBucket) and res.headers.get("X-RateLimit-Bucket"):
            if guild_id or channel_id:
                self.buckets[bucket_hash] = Bucket(
                    discord_hash=res.headers.get("X-RateLimit-Bucket")
                )  # Make a bucket
            else:
                b = Bucket(discord_hash=res.headers.get("X-RateLimit-Bucket"))
                if b in self.buckets.values():
                    self.buckets[bucket_hash] = {v: k for k, v in self.buckets.items()}[
                        b
                    ]
                else:
                    self.buckets[bucket_hash] = b
        body = {}
        if res.headers["Content-Type"] == "application/json":
            body = await res.json()
        else:
            body = await res.text()
        if (
            int(res.headers.get("X-RateLimit-Remaining", 1)) == 0
            and res.status != HTTPCodes.TOO_MANY_REQUESTS
        ):  # We've exhausted the bucket.
            logger.critical(
                f"Exhausted {res.headers['X-RateLimit-Bucket']} ({res.url}). Reset in {res.headers['X-RateLimit-Reset-After']} seconds"
            )
            await asyncio.sleep(float(res.headers["X-RateLimit-Reset-After"]))
            bucket.lock.release()

        if res.status == HTTPCodes.TOO_MANY_REQUESTS:  # Body is always present here.
            time_to_sleep = (
                body.get("retry_after")
                if body.get("retry_after") > res.headers["X-RateLimit-Reset-After"]
                else res.headers["X-RateLimit-Reset-After"]
            )

            logger.critical(f"Rate limited. Reset in {time_to_sleep} seconds")
            if res.headers["X-RateLimit-Scope"] == "global":
                await self.global_ratelimit.clear()

            await asyncio.sleep(time_to_sleep)

            await self.global_ratelimit.set()
            bucket.lock.release()
            return await self.request(
                method, url, *args, **kwargs, attempt=attempt + 1
            )  # Retry the request

        if res.status >= HTTPCodes.SERVER_ERROR:
            raise DiscordServerError5xx(body)

        elif res.status == HTTPCodes.NOT_FOUND:
            raise NotFound404(body)

        elif res.status == HTTPCodes.FORBIDDEN:
            raise Forbidden403(body)

        elif not 300 > res.status >= 200:
            raise DiscordAPIError(body)

        if bucket.lock.locked():
            try:
                bucket.lock.release()
            except Exception as e:
                logger.exception(e)

        async def dispose():  # After waiting 5 minutes without any interaction, the bucket will be disposed.
            await asyncio.sleep(300)
            try:
                del self.buckets[bucket_hash]
            except KeyError:
                ...

        bucket.close_task.cancel()

        bucket.close_task = asyncio.get_event_loop().create_task(dispose())

        return res

    @staticmethod
    async def log_request(res):
        message = [
            f"Sent a {res.request_info.method} to {res.url} "
            f"and got a {res.status} response. ",
            f"Content-Type: {res.headers['Content-Type']} ",
        ]

        if h := dict(res.headers):
            message.append(f"Received headers: {h} ")

        if h := dict(res.request_info.headers):
            message.append(f"Sent headers: {h} ")

        try:
            message.append(f"Received body: {await res.json()} ")

        except:
            ...

        finally:
            logger.debug("".join(message))

    async def get(
        self,
        url,
        *args,
        to_discord: bool = True,
        **kwargs,
    ):
        if to_discord:
            return await self.request("GET", url, *args, **kwargs)
        return await super().get(url, *args, **kwargs)

    async def post(self, url, *args, to_discord: bool = True, **kwargs):
        if to_discord:
            return await self.request("POST", url, *args, **kwargs)
        return await super().post(url, *args, **kwargs)

    async def patch(self, url, *args, to_discord: bool = True, **kwargs):
        if to_discord:
            res = await self.request("PATCH", url, *args, **kwargs)
            return res
        return await super().patch(url, *args, **kwargs)

    async def delete(self, url, *args, to_discord: bool = True, **kwargs):
        if to_discord:
            res = await self.request("DELETE", url, *args, **kwargs)
            return res
        return await super().delete(url, **kwargs)

    async def put(self, url, *args, to_discord: bool = True, **kwargs):
        if to_discord:
            res = await self.request("PUT", url, *args, **kwargs)
            return res
        return await super().put(url, *args, **kwargs)

from __future__ import annotations

import asyncio
from importlib.util import find_spec
from logging import getLogger
from typing import Any, Dict, List, Optional, Type, Union


from .buckets import TopLevelBucket, Bucket, MockBucket
from .. import __version__
from ..exceptions import BadRequest, Forbidden, HTTPException, NotFound, Unauthorized, TooManyRetries
from ..file import File
from ..utils import clear_none_values, json_serialize, clean_url
from .websocket import GatewayWebsocket

import aiohttp

logger = getLogger("EpikCord.http")


class Route:
    def __init__(
        self,
        method: str,
        url: str,
        *,
        channel_id: Optional[int] = None,
        guild_id: Optional[int] = None,
        webhook_id: Optional[int] = None,
        webhook_token: Optional[str] = None,
    ):
        self.method: str = method
        self.url: str = url
        self.channel_id: Optional[int] = channel_id
        self.guild_id: Optional[int] = guild_id
        self.webhook_id: Optional[int] = webhook_id
        self.webhook_token: Optional[str] = webhook_token
        self.major_parameters: Dict[str, Optional[Union[int, str]]] = clear_none_values(
            {
                "channel_id": channel_id,
                "guild_id": guild_id,
                "webhook_id": webhook_id,
                "webhook_token": webhook_token,
            }
        )

class HTTPClient:
    error_mapping: Dict[
        int,
        Union[Type[NotFound], Type[Forbidden], Type[Unauthorized], Type[BadRequest]],
    ] = {400: BadRequest, 401: Unauthorized, 403: Forbidden, 404: NotFound}

    def __init__(self, token: str, *, version: int = 10):
        self.token: str = token
        self.version: int = version
        self.session: aiohttp.ClientSession = aiohttp.ClientSession(
            headers={
                "Authorization": f"Bot {self.token}",
                "User-Agent": f"DiscordBot (https://github.com/EpikCord/EpikCord.py {__version__})",
            },
            json_serialize=json_serialize, # type: ignore
            ws_response_class=GatewayWebsocket,
        )
        self.buckets: Dict[str, Union[Bucket, TopLevelBucket]] = {}
        self.global_event: asyncio.Event = asyncio.Event()
        self.global_event.set()

    async def ws_connect(
        self, url: str, **kwargs
    ) -> aiohttp.ClientWebSocketResponse:
        return await self.session.ws_connect(url, **kwargs)

    async def request(
        self,
        route: Route,
        *args,
        discord: bool = True,
        json: Optional[Dict] = None,
        files: Optional[List[File]] = None,
        **kwargs,
    ) -> aiohttp.ClientResponse:
        """
        Parameters
        ----------
        *args
            The args to pass to the ClientSession.request method.
        discord: bool
            Whether this request is to Discord.
        json: Optional[Dict[:class:`str`, Any]]
            The json document to pass to the ClientSession.request method.
        files: Optional[List[File]]
            The files to pass to the request.
        **kwargs
            The kwargs to pass to the ClientSession.request method.

        Returns
        -------
        aiohttp.ClientResponse
            The response of the request.

        Raises
        ------
        NotFound
            If the request returns a 404 status code.
        Forbidden
            If the request returns a 403 status code.
        Unauthorized
            If the request returns a 401 status code.
        BadRequest
            If the request returns a 400 status code.
        HTTPException
            If the request returns a status code that is not OK and not any of the other exceptions.
        """

        method = route.method
        url = route.url

        if not discord:
            return await self.session.request(method, url, *args, **kwargs)

        self.setup_kwargs(kwargs, files=files, json=json)

        url = clean_url(url, self.version)
        bucket = self.buckets.get(f"{method}:{url}") or MockBucket()

        await self.global_event.wait()
        await bucket.wait()

        for _ in range(5):
            async with self.session.request(method, url, *args, **kwargs) as response:
                if isinstance(bucket, MockBucket):
                    bucket = await self.set_bucket(
                        response=response,
                        **route.major_parameters,
                    )

                data = await self.extract_content(response)

                await self.log_request(response, data)

                if response.status == 429:
                    await self.handle_ratelimit(data, bucket)
                elif response.headers.get("X-RateLimit-Remaining", "1") == "0":
                    await bucket.handle_exhaustion(int(response.headers["X-RateLimit-Reset-After"]))
                elif not response.ok:
                    error = self.error_mapping.get(response.status, HTTPException)
                    raise error(response, data)
                elif response.ok:
                    return response
        raise TooManyRetries(f"Attempted {method} request to {url} 5 times but failed.")

    async def set_bucket(
        self,
        *,
        response: aiohttp.ClientResponse,
        channel_id: Optional[int] = None,
        guild_id: Optional[int] = None,
        webhook_id: Optional[int] = None,
        webhook_token: Optional[str] = None,
    ) -> Union[Bucket, TopLevelBucket]:
        url = response.url
        method = response.method
        bucket_key: str = f"{method}:{url}"

        if channel_id or guild_id or webhook_id or webhook_token:
            bucket = TopLevelBucket(
                channel_id=channel_id,
                guild_id=guild_id,
                webhook_id=webhook_id,
                webhook_token=webhook_token,
                )

        else:

            bucket = Bucket(bucket_hash=response.headers["X-RateLimit-Bucket"])
            if bucket in self.buckets.values():
                self.buckets[bucket_key] = list(self.buckets.values())[
                    list(self.buckets.values()).index(bucket)
                ]
                bucket = self.buckets[bucket_key]
            self.buckets[bucket_key] = bucket

        return bucket

    @staticmethod
    async def extract_content(response: aiohttp.ClientResponse) -> Dict[str, Any]:
        if response.headers["Content-Type"] == "application/json":
            data = await response.json()
        else:
            data = {}
        return data

    async def handle_ratelimit(
        self, data: Dict[str, Any], bucket: Union[Bucket, TopLevelBucket]
    ):
        bucket.clear()

        if data["global"]:
            self.global_event.clear()

        await asyncio.sleep(data["retry_after"])

        self.global_event.set()
        bucket.set()

    @staticmethod
    async def log_request(res, body: Optional[dict] = None):
        messages = [
            f"Sent a {res.method} to {res.url} " f"and got a {res.status} response. ",
            f"Content-Type: {res.headers['Content-Type']} ",
        ]

        if body:
            messages.append(f"Sent body: {body} ")

        if h := dict(res.request_info.headers):
            messages.append(f"Sent headers: {h} ")

        if h := dict(res.headers):
            messages.append(f"Received headers: {h} ")

        try:
            messages.append(f"Received body: {await res.json()} ")

        finally:
            logger.debug("".join(messages))

    def setup_kwargs(
        self, kwargs, *, files: Optional[List[File]] = None, json: Optional[Dict] = None
    ) -> None:
        if not json and not files:
            return
        elif json and not files:
            kwargs["json"] = json
        elif files:
            if not json:
                json = {}
            form = aiohttp.FormData()
            json["attachments"] = []

            if files:
                for i, file in enumerate(files):
                    form.add_field(
                        f"files[{i}]",
                        file.contents,
                        filename=file.filename,
                        content_type=file.mime_type,
                    )
                    attachment = {
                        "filename": file.filename,
                        "id": i,
                    }
                    if file.description:
                        attachment["description"] = file.description

                    json["attachments"].append(attachment)

            form.add_field("payload_json", self.session.json_serialize(json))

            kwargs["data"] = form

    async def close(self) -> None:
        await self.session.close()

    async def get_gateway(self) -> str:
        response = await self.request(Route("GET", "/gateway"))
        return (await response.json())["url"]
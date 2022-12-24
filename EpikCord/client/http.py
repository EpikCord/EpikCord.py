from __future__ import annotations

from .. import __version__
from ..exceptions import NotFound, Forbidden, Unauthorized, BadRequest, HTTPException
from ..utils import clear_none_values

import asyncio
import mimetypes
from importlib.util import find_spec
from io import IOBase
from logging import getLogger
from typing import Optional, Dict, Any, Union, Type, List

_ORJSON = find_spec("orjson")

if _ORJSON:
    import orjson as json
else:
    import json

import aiohttp

logger = getLogger("EpikCord.http")

class File:
    def __init__(self, *, filename: str, contents: IOBase, mime_type: Optional[str] = None):
        """
        Parameters
        ----------
        filename: str
            The filename of the file.
        contents: IOBase
            The contents of the file.
        mime_type: Optional[str]
            The mime type of the file. If not provided, it will be guessed.
        """
        self.filename: str = filename
        self.contents: IOBase = contents
        self.mime_type: Optional[str] = mime_type or mimetypes.guess_type(filename)[0]

class MockBucket:
    async def wait(self):
        ...

    def clear(self):
        ...

    def set(self):
        ...

    def __eq__(self, other: MockBucket):
        return isinstance(other, MockBucket)


class Bucket:
    def __init__(self, *, bucket_hash: str):
        """
        Parameters
        ----------
        bucket_hash: str
            The bucket hash of the bucket provided by Discord.

        Attributes
        ----------
        bucket_hash: str
            The bucket hash of the bucket provided by Discord.
        event: asyncio.Event
            The event that is used to wait for the bucket to be set.
        """
        self.hash: str = bucket_hash
        self.event: asyncio.Event = asyncio.Event()
        self.event.set()

    async def wait(self):
        """
        Waits for the bucket to be set.
        """
        logger.info(f"Waiting for bucket {self.hash} to be set.")
        await self.event.wait()
        logger.info(f"Done waiting for bucket {self.hash}.")

    def set(self):
        """
        Sets the bucket.
        """
        logger.info(f"Setting bucket {self.hash}.")
        self.event.set()

    def clear(self):
        """
        Clears the bucket.
        """
        logger.info(f"Clearing bucket {self.hash}.")
        self.event.clear()

    def __eq__(self, other: Bucket):
        if isinstance(other, Bucket):
            return self.hash == other.hash
        return False


class TopLevelBucket:
    def __init__(self, *, major_parameters: Dict[str, Any]):
        """
        Parameters
        ----------
        major_parameters: Dict[str, Any]
            The major parameters for this Bucket

        Attributes
        ----------
        major_parameters: Dict[str, Any]
            The major parameters for this Bucket
        """
        self.event = asyncio.Event()
        self.event.set()
        self.major_parameters: Dict[str, Any] = major_parameters

    async def wait(self):
        """
        Waits for the bucket to be set.
        """
        logger.info(f"Waiting for bucket {self.major_parameters} to be set.")
        await self.event.wait()
        logger.info(f"Done waiting for bucket {self.major_parameters}.")

    def set(self):
        """
        Sets the bucket.
        """
        logger.info(f"Setting bucket {self.major_parameters}.")
        self.event.set()

    def clear(self):
        """
        Clears the bucket.
        """
        logger.info(f"Clearing bucket {self.major_parameters}.")
        self.event.clear()

    def __eq__(self, other: TopLevelBucket):
        if isinstance(other, TopLevelBucket):
            return self.major_parameters == other.major_parameters
        return False

    def __str__(self):
        return f"channel_id={self.major_parameters.get('channel_id')}, guild_id={self.major_parameters.get('guild_id')}, webhook_id={self.major_parameters.get('webhook_id')}, webhook_token={self.major_parameters.get('webhook_token')}"


class HTTPClient:
    error_mapping: Dict[
        int,
        Union[Type[NotFound], Type[Forbidden], Type[Unauthorized], Type[BadRequest]]
    ] = {400: BadRequest, 401: Unauthorized, 403: Forbidden, 404: NotFound}

    def __init__(self, token: str, *, version: int = 10):
        self.token: str = token
        self.version: int = version
        self.session: aiohttp.ClientSession = aiohttp.ClientSession(
            headers={
                "Authorization": f"Bot {self.token}",
                "User-Agent": f"DiscordBot (https://github.com/EpikCord/EpikCord.py {__version__})",
            },
            json_serialize=lambda x, *__, **___: json.dumps(x).decode("utf-8") # type: ignore
            if _ORJSON
            else json.dumps(x),
        )
        self.buckets: Dict[str, Union[Bucket, TopLevelBucket]] = {}
        self.global_event: asyncio.Event = asyncio.Event()
        self.global_event.set()

    async def ws_connect(
        self, url: str, headers: Dict = {}, **kwargs
    ) -> aiohttp.ClientWebSocketResponse:
        headers.update(
            {
                "User-Agent": f"DiscordBot (https://github.com/EpikCord/EpikCord.py {__version__})"
            }
        )
        return await self.session.ws_connect(url, headers=headers, **kwargs)

    async def request(
        self,
        method: str,
        url: str,
        *args,
        discord: bool = True,
        channel_id: Optional[int] = None,
        guild_id: Optional[int] = None,
        webhook_id: Optional[int] = None,
        webhook_token: Optional[str] = None,
        json: Optional[Dict] = None,
        files: Optional[List[File]] = None,
        **kwargs,
    ) -> Optional[aiohttp.ClientResponse]:
        """
        Parameters
        ----------
        method: str
            The method of the request.
        url: str
            The url of the request.
        *args
            The args to pass to the ClientSession.request method.
        discord: bool
            Whether this request is to Discord.
        channel_id: int
            The channel id of the request.
        guild_id: int
            The guild id of the request.
        webhook_id: int
            The webhook id of the request.
        webhook_token: str
            The webhook token of the request.
        json: Optional[Dict]
            The json to pass to the ClientSession.request method.
        files: Optional[List[File]]
            The files to pass to the request.
        **kwargs
            The kwargs to pass to the ClientSession.request method.

        Returns
        -------
        Optional[aiohttp.ClientResponse]
            The response of the request. Can be None if the request fails.

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

        if not discord:
            return await self.session.request(method, url, *args, **kwargs)

        url = self.clean_url(url)
        bucket = self.buckets.get(f"{method}:{url}") or MockBucket()

        await self.global_event.wait()
        await bucket.wait()

        for _ in range(5):
            if json and not files:
                kwargs["json"] = json
            else:
                form = aiohttp.FormData()
                if json:
                    form.add_field("payload_json", self.session.json_serialize(json))
                if files:
                    for i, file in enumerate(files):
                        form.add_field(
                            f"files[{i}]",
                            file.contents,
                            filename=file.filename,
                            content_type=file.mime_type,
                        )
                kwargs["data"] = form

            async with self.session.request(method, url, *args, **kwargs) as response:
                if isinstance(bucket, MockBucket):
                    bucket = await self.set_bucket(
                        response=response,
                        channel_id=channel_id,
                        guild_id=guild_id,
                        webhook_id=webhook_id,
                        webhook_token=webhook_token,
                    )

                data = await self.extract_content(response)

                if response.status == 429:
                    await self.handle_ratelimit(data, bucket)
                elif response.headers.get("X-RateLimit-Remaining", "1") == "0":
                    await self.handle_exhausted_bucket(response, bucket)
                elif not response.ok:
                    raise self.error_mapping[response.status](response, data)

                return response

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

        if channel_id or guild_id or webhook_id or webhook_token:
            bucket = TopLevelBucket(
                major_parameters=clear_none_values(
                    {
                        "channel_id": channel_id,
                        "guild_id": guild_id,
                        "webhook_id": webhook_id,
                        "webhook_token": webhook_token,
                    }
                )
            )

        else:

            bucket = Bucket(bucket_hash=response.headers["X-RateLimit-Bucket"])
            if bucket in self.buckets.values():
                self.buckets[f"{method}:{url}"] = list(self.buckets.values())[
                    list(self.buckets.values()).index(bucket)
                ]
                bucket = self.buckets[f"{method}:{url}"]
            self.buckets[f"{method}:{url}"] = bucket

        return bucket

    async def extract_content(self, response: aiohttp.ClientResponse) -> Dict[str, Any]:
        if response.headers["Content-Type"] == "application/json":
            data = await response.json()
        else:
            data = {}
        return data

    async def handle_exhausted_bucket(self, response: aiohttp.ClientResponse, bucket: Union[Bucket, TopLevelBucket]):
        bucket.clear()
        await asyncio.sleep(int(response.headers["X-RateLimit-Reset-After"]))
        bucket.set()

    async def handle_ratelimit(
        self, data: Dict[str, Any], bucket: Union[Bucket, TopLevelBucket]
    ):
        bucket.clear()

        if data["global"]:
            self.global_event.clear()

        await asyncio.sleep(data["retry_after"])

        self.global_event.set()
        bucket.set()

    def clean_url(self, url: str) -> str:
        if url.startswith("/"):
            url = f"https://discord.com/api/v{self.version}{url}"
        else:
            url = f"https://discord.com/api/v{self.version}/{url}"

        if url.endswith("/"):
            url = url[:-1]

        return url

    @staticmethod
    async def log_request(res, body: Optional[dict] = None):
        messages = [
            f"Sent a {res.method} to {res.url} "
            f"and got a {res.status} response. ",
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

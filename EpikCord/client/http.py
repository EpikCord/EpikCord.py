from __future__ import annotations

from ..exceptions import NotFound, Forbidden, Unauthorized, BadRequest, HTTPException
from ..utils import clear_none_values
import asyncio
from typing import Optional, Dict, Any, Union, Type

import aiohttp


class MockBucket:

    async def wait(self):
        ...

    def clear(self):
        ...

    def set(self):
        ...

    def __eq__(self, other: MockBucket):
        return isinstance(other, MockBucket):


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
        await self.event.wait()

    def set(self):
        """
        Sets the bucket.
        """
        self.event.set()

    def clear(self):
        """
        Clears the bucket.
        """
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
        await self.event.wait()

    def set(self):
        """
        Sets the bucket.
        """
        self.event.set()
    
    def clear(self):
        """
        Clears the bucket.
        """
        self.event.clear()

    def __eq__(self, other: TopLevelBucket):
        if isinstance(other, TopLevelBucket):
            return self.major_parameters == other.major_parameters
        return False


class HTTPClient:
    error_mapping: Dict[int, Union[Type[NotFound], Type[Forbidden], Type[Unauthorized], Type[BadRequest]]] = {
        400: BadRequest,
        401: Unauthorized,
        403: Forbidden,
        404: NotFound
    }
    def __init__(self, token: str, *, version: int = 10):
        self.token: str = token
        self.version: int = version
        self.session: aiohttp.ClientSession = aiohttp.ClientSession(
            headers={"Authorization": f"Bot {self.token}"}
        )
        self.buckets: Dict[str, Union[Bucket, TopLevelBucket]] = {}
        self.global_event: asyncio.Event = asyncio.Event()
        self.global_event.set()

    async def ws_connect(self, url: str) -> aiohttp.ClientWebSocketResponse:
        return await self.session.ws_connect(url)

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

        if url.startswith("/"):
            url = f"https://discord.com/api/v{self.version}{url}"
        else:
            url = f"https://discord.com/api/v{self.version}/{url}"

        if url.endswith("/"):
            url = url[:-1]

        bucket = self.buckets.get(f"{method}:{url}") or MockBucket()

        await self.global_event.wait()
        await bucket.wait()
        for _ in range(5):
            async with self.session.request(method, url, *args, **kwargs) as response:
                if isinstance(bucket, MockBucket):
                    bucket = await self.set_bucket(response=response, channel_id=channel_id, guild_id=guild_id, webhook_id=webhook_id, webhook_token=webhook_token)

                data = await self.extract_content(response)

                if response.status == 429:
                    await self.handle_ratelimit(data, bucket)
                elif not response.ok:
                    raise self.error_mapping[response.status](response, data)

                return response

    async def set_bucket(self, *, response: aiohttp.ClientResponse, channel_id: Optional[int] = None, guild_id: Optional[int] = None, webhook_id: Optional[int] = None, webhook_token: Optional[str] = None) -> Union[Bucket, TopLevelBucket]:
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

    async def handle_ratelimit(self, data: Dict[str, Any], bucket: Union[Bucket, TopLevelBucket]):
        bucket.clear()

        if data["global"]:
            self.global_event.clear()

        await asyncio.sleep(data["retry_after"])

        self.global_event.set()
        bucket.set()
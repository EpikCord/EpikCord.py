from __future__ import annotations

import asyncio
from enum import IntEnum
from logging import getLogger
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Type, TypedDict, Union

import aiohttp
from typing_extensions import NotRequired

from .. import __version__
from ..exceptions import (
    BadRequest,
    Forbidden,
    HTTPException,
    NotFound,
    TooManyRetries,
    Unauthorized,
)
from ..file import File
from ..utils import clean_url, clear_none_values, extract_content, json_serialize
from .buckets import Bucket, MockBucket, TopLevelBucket
from .websocket import GatewayWebSocket

if TYPE_CHECKING:
    from .client import TokenStore

logger = getLogger("EpikCord.http")


class APIVersion(IntEnum):
    """Represents the version of the Discord HTTP API and Gateway WebSocket to use."""

    NINE = 9
    TEN = 10


class SendingAttachmentData(TypedDict):
    """The data used to send an attachment."""

    id: int
    filename: str
    description: NotRequired[str]
    ephemeral: NotRequired[bool]


class MajorParameters:
    def __init__(
        self,
        channel_id: Optional[int] = None,
        guild_id: Optional[int] = None,
        webhook_id: Optional[int] = None,
        webhook_token: Optional[str] = None,
    ):
        """A class to group up all the major parameters of a route.

        Parameters
        ----------
        channel_id: Optional[int]
            The channel id in the route.
        guild_id: Optional[int]
            The guild id in the route.
        webhook_id: Optional[int]
            The webhook id in the route.
        webhook_token: Optional[str]
            The webhook token in the route.

        Attributes
        ----------
        channel_id: Optional[int]
            The channel id in the route.
        guild_id: Optional[int]
            The guild id in the route.
        webhook_id: Optional[int]
            The webhook id in the route.
        webhook_token: Optional[str]
            The webhook token in the route.
        major_parameters: Dict[str, Union[int, str]]
            The major parameters compiled into a single dictionary.
        """
        self.channel_id: Optional[int] = channel_id
        self.guild_id: Optional[int] = guild_id
        self.webhook_id: Optional[int] = webhook_id
        self.webhook_token: Optional[str] = webhook_token
        self.major_parameters: Dict[str, Union[int, str]] = clear_none_values(
            {
                "channel_id": self.channel_id,
                "guild_id": self.guild_id,
                "webhook_id": self.webhook_id,
                "webhook_token": self.webhook_token,
            }
        )

    def __eq__(self, other: Any):
        if isinstance(other, MajorParameters):
            return self.major_parameters == other.major_parameters
        return False


class Route:
    """Represents a HTTP route."""

    def __init__(
        self,
        method: str,
        url: str,
        *,
        major_parameters: MajorParameters = MajorParameters(),
    ):
        """
        Parameters
        ----------
        method: str
            The method of the route.
        url: str
            The url of the route.
        major_parameters: MajorParameters
            The major parameters of the route.

        Attributes
        ----------
        method: str
            The method of the route.
        url: str
            The url of the route.
        major_parameters: MajorParameters
            The major parameters of the route.
        """
        self.method: str = method
        self.url: str = url
        self.major_parameters: MajorParameters = major_parameters


class HTTPClient:
    """The HTTPClient used to make requests to the Discord API."""

    error_mapping: Dict[int, Type[HTTPException]] = {
        400: BadRequest,
        401: Unauthorized,
        403: Forbidden,
        404: NotFound,
    }

    def __init__(self, token: TokenStore, *, version: APIVersion = APIVersion.TEN):
        """
        Parameters
        ----------
        token: str
            The token of the bot. Used as authorization. Should be kept private at all times.
        version: int
            The version of the Discord API to use. Defaults to 10.

        Attributes
        ----------
        token: str
            The token of the bot. Used as authorization. Should be kept private at all times.
        version: int
            The version of the Discord API to use.
        session: aiohttp.ClientSession
            The ClientSession used to make requests.
        buckets: Dict[str, Union[Bucket, TopLevelBucket]]
            The buckets used to ratelimit requests.
        global_event: asyncio.Event
            The event used to wait for the global ratelimit to end.
        error_mapping: Dict[int, Type[HTTPException]]
            The mapping of status codes to exceptions.
        """
        self.token: TokenStore = token
        self.version: APIVersion = version
        self.session: aiohttp.ClientSession = aiohttp.ClientSession(
            headers={
                "Authorization": f"Bot {self.token}",
                "User-Agent": f"DiscordBot (https://github.com/EpikCord/EpikCord.py {__version__})",
            },
            json_serialize=json_serialize,  # type: ignore
            ws_response_class=GatewayWebSocket,
        )
        self.buckets: Dict[str, Union[Bucket, TopLevelBucket]] = {}
        self.global_event: asyncio.Event = asyncio.Event()
        self.global_event.set()

    async def ws_connect(self, url: str, **kwargs) -> GatewayWebSocket:
        return await self.session.ws_connect(url, **kwargs)  # type: ignore

    async def request(
        self,
        route: Route,
        *,
        json: Optional[Dict[str, Any]] = None,
        files: Optional[List[File]] = None,
        **kwargs,
    ) -> aiohttp.ClientResponse:
        """
        Parameters
        ----------
        route: Route
            The Route to make the request to.
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

        self.setup_request_kwargs(kwargs, files=files, json=json)

        url = clean_url(url, self.version.value)
        bucket = self.buckets.get(f"{method}:{url}") or MockBucket()

        await self.global_event.wait()
        await bucket.wait()

        for _ in range(5):
            async with self.session.request(method, url, **kwargs) as response:
                if isinstance(bucket, MockBucket) and response.headers.get(
                    "X-RateLimit-Bucket"
                ):
                    bucket = await self.set_bucket(
                        response=response, major_parameters=route.major_parameters
                    )

                data = await extract_content(response)

                await self.log_request(response, data)

                if response.status == 429:
                    await self.handle_ratelimit(data, bucket)
                elif response.headers.get("X-RateLimit-Remaining", "1") == "0":
                    await bucket.handle_exhaustion(
                        int(response.headers["X-RateLimit-Reset-After"])
                    )
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
        major_parameters: Optional[MajorParameters] = None,
    ) -> Union[Bucket, TopLevelBucket]:
        """Sets the bucket for the request.

        Parameters
        ----------
        response: aiohttp.ClientResponse
            The response of the request.
        major_parameters: Optional[MajorParameters]
            The major parameters of the request.

        Returns
        -------
        Union[Bucket, TopLevelBucket]
            The bucket for the request.
        """
        url = response.url
        method = response.method
        bucket_key: str = f"{method}:{url}"

        bucket: Optional[Union[Bucket, TopLevelBucket]] = None

        if major_parameters:
            bucket = TopLevelBucket(
                channel_id=major_parameters.channel_id,
                guild_id=major_parameters.guild_id,
                webhook_id=major_parameters.webhook_id,
                webhook_token=major_parameters.webhook_token,
            )
        else:
            bucket = Bucket(bucket_hash=response.headers["X-RateLimit-Bucket"])
            if bucket in self.buckets.values():
                listed_buckets = list(self.buckets.values())
                self.buckets[bucket_key] = listed_buckets[listed_buckets.index(bucket)]
                bucket = self.buckets[bucket_key]
            self.buckets[bucket_key] = bucket

        return bucket

    async def handle_ratelimit(
        self, data: Dict[str, Any], bucket: Union[Bucket, TopLevelBucket, MockBucket]
    ):
        """Handles the ratelimit for the request.

        Parameters
        ----------
        data: Dict[str, Any]
            The data in the response.
        bucket: Union[Bucket, TopLevelBucket, MockBucket]
            The bucket for the request.
        """
        bucket.clear()

        if data["global"]:
            self.global_event.clear()

        await asyncio.sleep(data["retry_after"])

        self.global_event.set()
        bucket.set()

    @staticmethod
    async def log_request(res, body: Optional[dict] = None):
        """Logs information about the request."""
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

    def add_file(
        self, form: aiohttp.FormData, file: File, i: int
    ) -> SendingAttachmentData:
        form.add_field(
            f"files[{i}]",
            file.contents,
            filename=file.filename,
            content_type=file.mime_type,
        )

        attachment: SendingAttachmentData = {
            "filename": file.filename,
            "id": i,
        }
        if file.description:
            attachment["description"] = file.description

        return attachment

    def setup_request_kwargs(
        self, kwargs, *, files: Optional[List[File]] = None, json: Optional[Dict] = None
    ) -> Optional[Dict]:
        """Sets up the request kwargs.

        Parameters
        ----------
        kwargs: Dict[str, Any]
            The kwargs for the request.
        files: Optional[List[File]]
            The files to send with the request.
        json: Optional[Dict]
            The json to send with the request.
        """
        if not json and not files:
            return None

        return_kwargs = kwargs.copy()

        if json and not files:
            return_kwargs["json"] = json
        elif files:
            if not json:
                json = {}
            form = aiohttp.FormData()
            json["attachments"] = []

            if files:
                for i, file in enumerate(files):
                    attachment = self.add_file(form, file, i)
                    json["attachments"].append(attachment)

            form.add_field("payload_json", self.session.json_serialize(json))

            return_kwargs["data"] = form

        return return_kwargs

    async def close(self) -> None:
        """Closes the session."""
        await self.session.close()

    async def get_gateway(self) -> str:
        """Gets the URL used for connecting to the Gateway.

        Returns
        -------
        str
            The URL used for connecting to the Gateway.
        """
        response = await self.request(Route("GET", "/gateway"))
        data = await response.json()
        return data["url"]

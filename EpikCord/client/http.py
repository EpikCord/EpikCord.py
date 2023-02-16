from __future__ import annotations

import asyncio
from enum import IntEnum
from logging import getLogger
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Type, Union

import aiohttp
from discord_typings import GetGatewayBotData, SessionStartLimitData

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
from ..utils import (
    HTTPCodes,
    add_file,
    clean_url,
    extract_content,
    json_serialize,
    log_request,
)
from .rate_limit_tools import (
    Bucket,
    MajorParameters,
    MockBucket,
    Route,
    TopLevelBucket,
)
from .websocket import GatewayWebSocket

if TYPE_CHECKING:
    from .client import TokenStore

logger = getLogger("EpikCord.http")


class APIVersion(IntEnum):
    """The version of the Discord HTTP API and Gateway WebSocket to use."""

    NINE = 9
    TEN = 10


class SessionStartLimit:
    """Represents the session start limit data.

    Attributes
    ----------
    total: int
        Total number of sessions that can be started in a 24 hour period.
    remaining: int
        Remaining sessions left in 24 hours.
    reset_after: int
        Time in seconds until session limit reset
    max_concurrency: int
        Maximum of IDENTIFY requests that can be sent in 5 seconds.
    """

    def __init__(self, data: SessionStartLimitData):
        """
        Parameters
        ----------
        data: SessionStartLimitData
            The data returned by the Discord API.
        """

        self.total: int = data["total"]
        self.remaining: int = data["remaining"]
        self.reset_after: int = data["reset_after"]
        self.max_concurrency: int = data["max_concurrency"]


class GatewayBotData:
    """Represents the data returned by the Get Gateway Bot endpoint.

    Attributes
    ----------
    url: str
        The URL to use for connecting to the gateway.
    shards: int
        The recommended amount of shards to use.
    session_start_limit: SessionStartLimit
        The session start limit data.
    """

    def __init__(self, data: GetGatewayBotData):
        """
        Parameters
        ----------
        data: GetGatewayBotData
            The data returned by the Discord API.
        """

        self.url: str = data["url"]
        self.shards: int = data["shards"]
        self.session_start_limit: SessionStartLimit = SessionStartLimit(
            data["session_start_limit"]
        )


class HTTPClient:
    """The HTTPClient used to make requests to the Discord API.

    Attributes
    ----------
    token: str
        The token of the bot. Used as authorization.
        Should be kept private at all times.
    version: int
        The version of the Discord API to use.
    session: aiohttp.ClientSession
        The underlying session used to make HTTP requests.
    global_event: asyncio.Event
        The Event used to implement global ratelimits.
    buckets: Dict[str, Union[Bucket, TopLevelBucket]]
        A mapping of bucket hashes to Bucket instances.
    error_mapping: Dict[HTTPCodes, Type[HTTPException]]
        A mapping of HTTP status codes to their respective exceptions.
    """

    error_mapping: Dict[HTTPCodes, Type[HTTPException]] = {
        HTTPCodes.BAD_REQUEST: BadRequest,
        HTTPCodes.UNAUTHORIZED: Unauthorized,
        HTTPCodes.FORBIDDEN: Forbidden,
        HTTPCodes.NOT_FOUND: NotFound,
    }

    def __init__(
        self, token: TokenStore, *, version: APIVersion = APIVersion.TEN
    ):
        """
        Parameters
        ----------
        token: str
            The token of the bot. Used as authorization.
            Should be kept private at all times.
        version: int
            The version of the Discord API to use. Defaults to 10.
        """
        self.token: TokenStore = token
        self.version: APIVersion = version
        self.session: aiohttp.ClientSession = aiohttp.ClientSession(
            headers={
                "Authorization": f"Bot {self.token.value}",
                "User-Agent": (
                    "DiscordBot "
                    f"(https://github.com/EpikCord/EpikCord.py {__version__})"
                ),
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
            Generic Exception for unhandled errors that may occur.
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
                        response=response,
                        major_parameters=route.major_parameters,
                    )

                data = await extract_content(response)
                await log_request(response, data)

                if response.status == HTTPCodes.TOO_MANY_REQUESTS:
                    await self.handle_ratelimit(data, bucket)
                elif response.headers.get("X-RateLimit-Remaining", "1") == "0":
                    await bucket.handle_exhaustion(
                        int(response.headers["X-RateLimit-Reset-After"])
                    )
                elif not response.ok:
                    error = self.error_mapping.get(
                        HTTPCodes(response.status), HTTPException
                    )
                    raise error(data)
                elif response.ok:
                    return response
        raise TooManyRetries(
            f"Attempted {method} request to {url} 5 times but failed."
        )

    async def set_bucket(
        self,
        *,
        response: aiohttp.ClientResponse,
        major_parameters: Optional[MajorParameters] = None,
    ) -> Union[Bucket, TopLevelBucket]:
        """Set the bucket for the request.

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
        bucket: Union[Bucket, TopLevelBucket]

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
                self.buckets[bucket_key] = listed_buckets[
                    listed_buckets.index(bucket)
                ]
                bucket = self.buckets[bucket_key]
            self.buckets[bucket_key] = bucket

        return bucket

    async def handle_ratelimit(
        self,
        data: Dict[str, Any],
        bucket: Union[Bucket, TopLevelBucket, MockBucket],
    ):
        """Handle the ratelimit for the request.

        Parameters
        ----------
        data: Dict[str, Any]
            The data in the response.
        bucket: Union[Bucket, TopLevelBucket, MockBucket]
            The bucket for the request.
        """
        logger.critical(
            f"Rate-limited bucket {bucket} for {data['retry_after']} seconds."
        )
        bucket.clear()

        if data["global"]:
            self.global_event.clear()

        await asyncio.sleep(data["retry_after"])

        self.global_event.set()
        bucket.set()

    def setup_request_kwargs(
        self,
        kwargs,
        *,
        files: Optional[List[File]] = None,
        json: Optional[Dict] = None,
    ) -> Optional[Dict]:
        """Set up the request kwargs.

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
                    attachment = add_file(form, file, i)
                    json["attachments"].append(attachment)

            form.add_field("payload_json", self.session.json_serialize(json))

            return_kwargs["data"] = form

        return return_kwargs

    async def close(self) -> None:
        """Close the session."""
        await self.session.close()

    async def get_gateway(self) -> str:
        """Get the URL used for connecting to the Gateway.

        Returns
        -------
        str
            The URL used for connecting to the Gateway.
        """
        response = await self.request(Route("GET", "/gateway"))
        data = await response.json()
        return data["url"]

    async def get_gateway_bot(self) -> GatewayBotData:
        """Gets information and recommendations for connecting to the Gateway.

        Returns
        -------
        GatewayBotData
            The data returned from the request.
        """
        response = await self.request(Route("GET", "/gateway/bot"))
        data = await response.json()
        return GatewayBotData(data)

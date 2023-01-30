from __future__ import annotations

import asyncio
from datetime import timedelta
from logging import getLogger
from typing import Any, Dict, Optional, Union

from ..ext import tasks
from ..utils import clear_none_values

logger = getLogger("EpikCord.http")


class GatewayRateLimiter:
    def __init__(self):

        self.event = asyncio.Event()
        self.event.set()

        self.remaining = 120
        self.limit = 120

    @tasks.task(duration=timedelta(seconds=60))
    async def reset(self):
        self.remaining = self.limit
        self.event.set()

    async def tick(self):
        await self.event.wait()
        self.remaining -= 1
        if self.remaining == 0:
            self.event.clear()


class MockBucket:
    """A mock bucket that does nothing."""

    async def wait(self):
        """Pretends to wait for the Event to be set"""
        ...

    def clear(self):
        """Pretends to clear the Event"""
        ...

    def set(self):
        """Pretends to set the Event"""
        ...

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, MockBucket)

    async def handle_exhaustion(self, retry_after: int):
        """Pretends to handle the exhaustion of the bucket"""
        ...


class Bucket:
    """
    Attributes
    ----------
    hash: str
        The bucket hash of the bucket provided by Discord.
    event: asyncio.Event
        The event that is used to wait for the bucket to be set.
    """

    def __init__(self, *, bucket_hash: str):
        """
        Parameters
        ----------
        bucket_hash: str
            The bucket hash of the bucket provided by Discord.
        """
        self.hash: str = bucket_hash
        self.event: asyncio.Event = asyncio.Event()
        self.event.set()

    async def wait(self):
        """
        Waits for the Event to be set.
        """
        logger.info(f"Waiting for bucket {self.hash} to be set.")
        await self.event.wait()
        logger.info(f"Done waiting for bucket {self.hash}.")

    def set(self):
        """
        Sets the Event.
        """
        logger.info(f"Setting bucket {self.hash}.")
        self.event.set()

    def clear(self):
        """
        Clears the Event.
        """
        logger.info(f"Clearing bucket {self.hash}.")
        self.event.clear()

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Bucket):
            return self.hash == other.hash
        return False

    async def handle_exhaustion(self, retry_after: int):
        """
        Handles the exhaustion of the bucket.

        Parameters
        ----------
        retry_after: int
            The amount of time to wait before retrying.
        """
        self.clear()
        logger.info(
            f"Bucket {self.hash} exhausted, waiting {retry_after} seconds."
        )
        await asyncio.sleep(retry_after)
        self.set()


class TopLevelBucket:
    """
    Attributes
    ----------
    channel_id: Optional[int]
        The channel ID of the bucket.
    guild_id: Optional[int]
        The guild ID of the bucket.
    webhook_id: Optional[int] = None
        The webhook ID of the bucket.
    webhook_token: Optional[str]
        The webhook token of the bucket.
    major_parameters: Dict[str, Any]
        The major parameters for this Bucket
    event: asyncio.Event
        The event that is used to wait for the bucket to be set.
    """

    def __init__(
        self,
        *,
        channel_id: Optional[int] = None,
        guild_id: Optional[int] = None,
        webhook_id: Optional[int] = None,
        webhook_token: Optional[str] = None,
    ):
        """
        Parameters
        ----------
        channel_id: Optional[int]
            The channel ID of the bucket.
        guild_id: Optional[int]
            The guild ID of the bucket.
        webhook_id: Optional[int] = None
            The webhook ID of the bucket.
        webhook_token: Optional[str]
            The webhook token of the bucket.
        """
        self.event = asyncio.Event()
        self.event.set()
        self.channel_id: Optional[int] = channel_id
        self.guild_id: Optional[int] = guild_id
        self.webhook_id: Optional[int] = webhook_id
        self.webhook_token: Optional[str] = webhook_token
        self.major_parameters: Dict[
            str, Optional[Union[int, str]]
        ] = clear_none_values(
            {
                "channel_id": channel_id,
                "guild_id": guild_id,
                "webhook_id": webhook_id,
                "webhook_token": webhook_token,
            }
        )

    async def wait(self):
        """
        Waits for the Event to be set.
        """
        logger.info(f"Waiting for bucket {self.major_parameters} to be set.")
        await self.event.wait()
        logger.info(f"Done waiting for bucket {self.major_parameters}.")

    def set(self):
        """
        Sets the Event.
        """
        logger.info(f"Setting bucket {self.major_parameters}.")
        self.event.set()

    def clear(self):
        """
        Clears the Event.
        """
        logger.info(f"Clearing bucket {self.major_parameters}.")
        self.event.clear()

    def __eq__(self, other: Any):
        if isinstance(other, TopLevelBucket):
            return self.major_parameters == other.major_parameters
        return False

    def __str__(self) -> str:
        return (
            f"{self.channel_id}:{self.guild_id}"
            f":{self.webhook_id}:{self.webhook_token}"
        )

    async def handle_exhaustion(self, retry_after: int):
        """
        Handles the exhaustion of the bucket.

        Parameters
        ----------
        retry_after: int
            The amount of time to wait before retrying.
        """
        self.clear()
        logger.info(
            f"Bucket {str(self)} exhausted, waiting {retry_after} seconds."
        )
        await asyncio.sleep(retry_after)
        self.set()


class MajorParameters:
    """A class to group up all the major parameters of a route.

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

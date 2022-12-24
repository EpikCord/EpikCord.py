from __future__ import annotations

from ..utils import clear_none_values

import asyncio
from logging import getLogger
from typing import Union, Optional, Dict

import aiohttp

logger = getLogger("EpikCord.http")

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

    async def handle_exhaustion(self, retry_after: int):
        """
        Handles the exhaustion of the bucket.

        Parameters
        ----------
        retry_after: int
            The amount of time to wait before retrying.
        """
        self.clear()
        logger.info(f"Bucket {self.hash} exhausted, waiting {retry_after} seconds.")
        await asyncio.sleep(retry_after)
        self.set()

class TopLevelBucket:
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
        self.event = asyncio.Event()
        self.event.set()
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
        return (
            f"{self.channel_id}:{self.guild_id}:{self.webhook_id}:{self.webhook_token}"
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
        logger.info(f"Bucket {str(self)} exhausted, waiting {retry_after} seconds.")
        await asyncio.sleep(retry_after)
        self.set()
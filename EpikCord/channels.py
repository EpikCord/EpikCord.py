from __future__ import annotations

from logging import getLogger
from typing import TYPE_CHECKING, Dict, List, Optional, Union

from .abstract import BaseChannel, Connectable, GuildChannel, Messageable
from .partials import PartialUser
from .thread import Thread

logger = getLogger(__name__)

if TYPE_CHECKING:
    import discord_typings


class Overwrite:
    def __init__(self, data: discord_typings.PermissionOverwriteData):
        self.id: int = int(data["id"])
        self.type: int = data["type"]
        self.allow: str = data["allow"]
        self.deny: str = data["deny"]


class GuildTextChannel(GuildChannel, Messageable):
    def __init__(
        self,
        client,
        data: Union[
            discord_typings.TextChannelData,
            discord_typings.NewsChannelData,
            discord_typings.ThreadChannelData,
            discord_typings.VoiceChannelData,
            discord_typings.ForumChannelData,
        ],
    ):
        super().__init__(client, data)
        Messageable.__init__(self, client, self.id)
        self.topic: Optional[str] = data.get("topic")  # type: ignore
        self.rate_limit_per_user: Optional[int] = data["rate_limit_per_user"] if data.get("rate_limit_per_user") else None  # type: ignore
        self.last_message_id: Optional[int] = int(data["last_message_id"]) if data.get("last_message_id") else None  # type: ignore
        self.default_auto_archive_duration: Optional[int] = data.get("default_auto_archive_duration")  # type: ignore # MyPy being absolutely dumb.

    async def start_thread(
        self,
        name: str,
        *,
        auto_archive_duration: Optional[int] = None,
        type: Optional[int] = 11,
        invitable: Optional[bool] = None,
        rate_limit_per_user: Optional[int] = None,
        reason: Optional[str] = None,
    ) -> Thread:
        data = self.client.utils.filter_values(
            {
                "name": name,
                "auto_archive_duration": auto_archive_duration,
                "type": type,
                "invitable": invitable,
                "rate_limit_per_user": rate_limit_per_user,
            }
        )

        headers = self.client.http.headers.copy()

        if reason:
            headers["X-Audit-Log-Reason"] = reason

        response = await self.client.http.post(
            f"/channels/{self.id}/threads",
            json=data,
            headers=headers,
            channel_id=self.id,
        )
        thread = Thread(self.client, await response.json())
        self.client.guilds[self.guild_id].channels.append(thread)

        return thread

    async def bulk_delete(self, message_ids: List[str], reason: Optional[str]) -> None:

        if reason:
            headers = self.client.http.headers.copy()
            headers["X-Audit-Log-Reason"] = reason

        response = await self.client.http.post(
            f"channels/{self.id}/messages/bulk-delete",
            json={"messages": message_ids},
            headers=headers,
            channel_id=self.id,
        )
        return await response.json()

    async def list_public_archived_threads(
        self, *, before: Optional[str] = None, limit: Optional[int] = None
    ) -> List[Thread]:

        params: Dict[str, Union[int, str]] = {}

        if before:
            params["before"] = before

        if limit:
            params["limit"] = limit

        response = await self.client.http.get(
            f"/channels/{self.id}/threads/archived/public",
            params=params,
            channel_id=self.id,
        )
        return [Thread(self.client, data) for data in await response.json()]

    async def list_private_archived_threads(
        self, *, before: Optional[int] = None, limit: Optional[int] = None
    ) -> List[Thread]:
        params: Dict[str, Optional[int]] = {}

        if before:
            params["before"] = before

        if limit is not None:
            params["limit"] = limit

        response = await self.client.http.get(
            f"/channels/{self.id}/threads/archived/private",
            params=params,
            channel_id=self.id,
        )
        return [Thread(self.client, data) for data in await response.json()]

    async def list_joined_private_archived_threads(
        self, *, before: Optional[int] = None, limit: Optional[int] = None
    ) -> List[Thread]:
        params: Dict[str, Union[int, str]] = {}

        if before:
            params["before"] = before

        if limit is not None:
            params["limit"] = limit

        response = await self.client.http.get(
            f"/channels/{self.id}/threads/archived/private",
            params=params,
            channel_id=self.id,
        )
        return [Thread(self.client, data) for data in await response.json()]


class GuildNewsChannel(GuildTextChannel):
    def __init__(self, client, data: discord_typings.NewsChannelData):
        super().__init__(client, data)
        self.default_auto_archive_duration: int = data["default_auto_archive_duration"]

    async def follow(self, webhook_channel_id: str):
        response = await self.client.http.post(
            f"/channels/{self.id}/followers",
            json={"webhook_channel_id": webhook_channel_id},
            channel_id=self.id,
        )
        return await response.json()


class DMChannel(BaseChannel):
    def __init__(self, client, data: discord_typings.DMChannelData):
        super().__init__(client, data)
        self.recipients: Optional[List[PartialUser]] = (
            [PartialUser(r) for r in data["recipients"]]
            if data.get("recipient")
            else None
        )


class CategoryChannel(GuildChannel):
    def __init__(self, client, data: discord_typings.CategoryChannelData):
        super().__init__(client, data)


class GuildNewsThread(Thread, GuildNewsChannel):
    def __init__(self, client, data):
        super().__init__(client, data)


class GuildStageChannel(BaseChannel):
    def __init__(self, client, data):
        super().__init__(client, data)
        self.guild_id: int = int(data["guild_id"])
        self.channel_id: int = int(data["channel_id"])
        self.privacy_level: discord_typings.StageInstancePrivacyLevels = data[
            "privacy_level"
        ]
        self.discoverable_disabled: bool = data["discoverable_disabled"]


class VoiceChannel(GuildChannel, Messageable, Connectable):  # type: ignore
    def __init__(self, client, data: discord_typings.VoiceChannelData):
        super().__init__(client, data)
        self.bitrate: int = data["bitrate"]
        self.user_limit: int = data["user_limit"]
        self.rtc_region: Optional[str] = data.get("rtc_region")


class ForumChannel(GuildChannel):
    def __init__(self, client, data):
        raise NotImplementedError("Forum channels are not implemented yet.")


AnyChannel = Union[
    GuildTextChannel,
    VoiceChannel,
    CategoryChannel,
    GuildNewsChannel,
    GuildNewsThread,
    Thread,
    GuildStageChannel,
    ForumChannel,
]

__all__ = (
    "Overwrite",
    "GuildTextChannel",
    "GuildNewsChannel",
    "DMChannel",
    "CategoryChannel",
    "GuildNewsThread",
    "GuildStageChannel",
    "VoiceChannel",
    "ForumChannel",
    "AnyChannel",
)

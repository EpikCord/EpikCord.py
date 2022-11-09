from __future__ import annotations

import datetime
from logging import getLogger
from typing import TYPE_CHECKING, Dict, List, Optional, Union, overload

from .abstract import BaseChannel, Connectable, Messageable
from .flags import ChannelFlags
from .partials import PartialUser
from .thread import Thread
from .user import User

logger = getLogger(__name__)

if TYPE_CHECKING:
    import discord_typings

    from .client import Client
    from .guild import Guild
    from .message import Message


class Overwrite:
    def __init__(self, data: discord_typings.PermissionOverwriteData):
        self.id: int = int(data["id"])
        self.type: int = data["type"]
        self.allow: str = data["allow"]
        self.deny: str = data["deny"]


class BaseGuildChannel(BaseChannel):
    def __init__(
        self,
        client: Client,
        data: Union[
            discord_typings.TextChannelData,
            discord_typings.VoiceChannelData,
            discord_typings.CategoryChannelData,
            discord_typings.NewsChannelData,
            discord_typings.ForumChannelData,
        ],
    ):

        super().__init__(client, data)
        self.guild_id: Optional[int] = (
            int(data["guild_id"]) if data.get("guild_id") else None
        )
        self.guild: Optional[Guild] = (
            self.client.guilds.get(self.guild_id) if self.guild_id else None
        )
        self.position: int = data["position"]
        self.permission_overwrites: List[Overwrite] = [
            Overwrite(overwrite) for overwrite in data["permission_overwrites"]
        ]
        self.name: str = data["name"]
        self.nsfw: bool = data["nsfw"]

    async def delete(self, *, reason: Optional[str] = None) -> None:

        response = await self.client.http.delete(
            f"/channels/{self.id}", channel_id=self.id, reason=reason
        )
        return await response.json()

    async def fetch_invites(self):
        response = await self.client.http.get(
            f"/channels/{self.id}/invites", channel_id=self.id
        )
        return await response.json()

    async def create_invite(
        self,
        *,
        max_age: Optional[int] = None,
        max_uses: Optional[int] = None,
        temporary: Optional[bool] = None,
        unique: Optional[bool] = None,
        target_type: Optional[int] = None,
        target_user_id: Optional[str] = None,
        target_application_id: Optional[str] = None,
    ):
        data = self.client.utils.filter_values(
            {
                "max_age": max_age,
                "max_uses": max_uses,
                "temporary": temporary,
                "unique": unique,
                "target_type": target_type,
                "target_user_id": target_user_id,
                "target_application_id": target_application_id,
            }
        )

        await self.client.http.post(
            f"/channels/{self.id}/invites", json=data, channel_id=self.id
        )

    async def delete_overwrite(self, overwrites) -> None:
        response = await self.client.http.delete(
            f"/channels/{self.id}/permissions/{overwrites.id}", channel_id=self.id
        )
        return await response.json()


class CommonFieldsTextAndNews(Messageable):
    def __init__(
        self,
        client: Client,
        data: Union[discord_typings.NewsChannelData, discord_typings.TextChannelData],
    ):
        super().__init__(client, int(data["id"]))
        self.topic: Optional[str] = data["topic"]
        self.parent_id: Optional[int] = (
            int(data["parent_id"]) if data["parent_id"] else None
        )
        self.last_pin_timestamp: Optional[datetime.datetime] = datetime.datetime.fromisoformat(data["last_pin_timestamp"]) if data.get("last_pin_timestamp") else None  # type: ignore
        self.default_auto_archive_duration: Optional[int] = data.get(
            "default_auto_archive_duration"
        )
        self.flags: ChannelFlags = ChannelFlags(data["flags"])


class GuildTextChannel(BaseGuildChannel, CommonFieldsTextAndNews):
    def __init__(self, client: Client, data: discord_typings.TextChannelData):
        super().__init__(client, data)
        CommonFieldsTextAndNews.__init__(self, client, data)
        self.rate_limit_per_user: int = data["rate_limit_per_user"]


class NewsChannel(BaseGuildChannel, CommonFieldsTextAndNews):
    def __init__(self, client: Client, data: discord_typings.NewsChannelData):
        super().__init__(client, data)
        CommonFieldsTextAndNews.__init__(self, client, data)


GuildAnnouncementChannel = NewsChannel


class DMChannel(Messageable):
    def __init__(self, client: Client, data: discord_typings.DMChannelData):
        super().__init__(client, int(data["id"]))
        self.recipients: List[User] = [
            User(client, user) for user in data["recipients"]
        ]
        self.last_pin_timestamp: Optional[datetime.datetime] = datetime.datetime.fromisoformat(data["last_pin_timestamp"]) if data.get("last_pin_timestamp") else None  # type: ignore
        self.flags: ChannelFlags = ChannelFlags(data["flags"])


class GroupDMChannel(Messageable):
    def __init__(self, client: Client, data: discord_typings.GroupDMChannelData):
        super().__init__(client, int(data["id"]))
        self.name: str = data["name"]
        self.recipients: List[User] = [
            User(client, user) for user in data["recipients"]
        ]
        self.icon: Optional[str] = data["icon"]
        self.owner_id: int = int(data["owner_id"])
        self.application_id: Optional[int] = (
            int(data["application_id"]) if data["application_id"] else None
        )
        self.last_pin_timestamp: Optional[datetime.datetime] = datetime.datetime.fromisoformat(data["last_pin_timestamp"]) if data.get("last_pin_timestamp") else None  # type: ignore
        self.flags: ChannelFlags = ChannelFlags(data["flags"])


class VoiceChannel(BaseGuildChannel, Connectable):
    def __init__(self, client: Client, data: discord_typings.VoiceChannelData):
        super().__init__(client, data)
        Connectable.__init__(self, client, channel=self)
        self.bitrate: int = data["bitrate"]
        self.user_limit: int = data["user_limit"]
        self.parent_id: Optional[int] = (
            int(data["parent_id"]) if data["parent_id"] else None
        )
        self.last_pin_timestamp: Optional[datetime.datetime] = datetime.datetime.fromisoformat(data["last_pin_timestamp"]) if data.get("last_pin_timestamp") else None  # type: ignore
        self.rtc_region: Optional[str] = data["rtc_region"]
        self.video_quality_mode: Optional[int] = data.get("video_quality_mode")
        self.flags: ChannelFlags = ChannelFlags(data["flags"])


class CategoryChannel(BaseGuildChannel):
    def __init__(self, client: Client, data: discord_typings.CategoryChannelData):
        self.flags: ChannelFlags = ChannelFlags(data["flags"])


class ForumChannel(BaseGuildChannel):
    def __init__(self, client: Client, data: discord_typings.ForumChannelData):
        super().__init__(client, data)
        self.topic: Optional[str] = data["topic"]
        self.rate_limit_per_user: int = data["rate_limit_per_user"]
        self.default_auto_archive_duration: Optional[int] = data.get(
            "default_auto_archive_duration"
        )
        self.flags: ChannelFlags = ChannelFlags(data["flags"])
        self.default_reaction_emoji: Optional[
            discord_typings.DefaultReactionData
        ] = data.get("default_reaction_emoji")
        self.default_thread_rate_limit_per_user: int = data[
            "default_thread_rate_limit_per_user"
        ]
        self.default_sort_order: Optional[discord_typings.SortOrderTypes] = data[
            "default_sort_order"
        ]


class GuildStageChannel(BaseGuildChannel, Connectable):
    def __init__(
        self,
        client: Client,
        data: Union[
            discord_typings.VoiceChannelData, discord_typings.InviteStageInstanceData
        ],
    ):
        super().__init__(client, data)
        Connectable.__init__(self, client, channel=self)
        self.bitrate: int = data["bitrate"]
        self.user_limit: int = data["user_limit"]
        self.parent_id: Optional[int] = (
            int(data["parent_id"]) if data["parent_id"] else None
        )
        self.last_pin_timestamp: Optional[datetime.datetime] = datetime.datetime.fromisoformat(data["last_pin_timestamp"]) if data.get("last_pin_timestamp") else None  # type: ignore
        self.rtc_region: Optional[str] = data["rtc_region"]
        self.video_quality_mode: Optional[int] = data.get("video_quality_mode")


AnyChannel = Union[
    GuildTextChannel,
    VoiceChannel,
    CategoryChannel,
    NewsChannel,
    Thread,
    GuildStageChannel,
    ForumChannel,
    GroupDMChannel,
]

__all__ = (
    "Overwrite",
    "GuildTextChannel",
    "GuildAnnouncementChannel",
    "DMChannel",
    "CategoryChannel",
    "GuildStageChannel",
    "VoiceChannel",
    "ForumChannel",
    "NewsChannel",
    "AnyChannel",
)

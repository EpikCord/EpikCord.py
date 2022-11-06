from __future__ import annotations

from logging import getLogger
from typing import TYPE_CHECKING, Dict, List, Optional, Union

from .abstract import BaseChannel, Connectable, Messageable
from .partials import PartialUser
from .thread import Thread

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

class GuildChannel(BaseChannel):
    def __init__(
        self,
        client: Client,
        data: Union[
            discord_typings.TextChannelData,
            discord_typings.NewsChannelData,
            discord_typings.VoiceChannelData,
            discord_typings.ForumChannelData
        ]
    ):
        super().__init__(client, data)
        self.guild_id: Optional[int] = int(data["guild_id"]) if data.get("guild_id") else None
        self.guild: Optional[Guild] = client.guilds.get(self.guild_id) if self.guild_id else None
        self.position: Optional[int] = data.get("position")
        self.permission_overwrites: Optional[List[Overwrite]] = [
            Overwrite(overwrite) for overwrite in data["permission_overwrites"]
        ] if data.get("permission_overwrites") else None
        


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


class GuildTextChannel(GuildChannel, Messageable):
    def __init__(self, client: Client, data: discord_typings.TextChannelData):
        super().__init__(client, data)
        Messageable.__init__(self, client, int(data["id"]))
        self.client: Client = client
        self.data: discord_typings.TextChannelData = data


AnyChannel = Union[
    GuildTextChannel,
    VoiceChannel,
    CategoryChannel,
    GuildAnnouncementChannel,
    GuildAnnouncementThread,
    Thread,
    GuildStageChannel,
    ForumChannel,
]

__all__ = (
    "Overwrite",
    "GuildTextChannel",
    "GuildAnnouncementChannel",
    "DMChannel",
    "CategoryChannel",
    "GuildAnnouncementThread",
    "GuildStageChannel",
    "VoiceChannel",
    "ForumChannel",
    "AnyChannel",
)


a
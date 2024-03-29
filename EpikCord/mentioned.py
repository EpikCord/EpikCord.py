from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from .user import User

if TYPE_CHECKING:
    import discord_typings


class MentionedUser(User):
    def __init__(self, client, data: discord_typings.UserMentionData):
        from EpikCord import GuildMember

        super().__init__(client, data)
        self.member: Optional[GuildMember] = (
            GuildMember(client, data["member"]) if data.get("member") else None
        )


class MentionedChannel:
    def __init__(self, data: discord_typings.ChannelMentionData):
        self.id: int = int(data["id"])
        self.guild_id: int = int(data["guild_id"])
        self.type: int = data["type"]
        self.name: str = data["name"]


__all__ = ("MentionedUser", "MentionedChannel")

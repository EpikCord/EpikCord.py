from typing import Optional
from .user import User


class MentionedUser(User):
    def __init__(self, client, data: dict):
        from EpikCord import GuildMember

        super().__init__(client, data)
        self.member: Optional[GuildMember] = (
            GuildMember(client, data["member"]) if data.get("member") else None
        )


class MentionedChannel:
    def __init__(self, data: dict):
        self.id: str = data["id"]
        self.guild_id: str = data["guild_id"]
        self.type: int = data["type"]
        self.name: str = data["name"]


__all__ = ("MentionedUser", "MentionedChannel")

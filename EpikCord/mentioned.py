from typing import Optional
from .user import User

class MentionedUser(User):
    def __init__(self, client, data: dict):
        from EpikCord import GuildMember
        super().__init__(client, data)
        self.member: Optional[GuildMember] = (
            GuildMember(client, data.get("member")) if data.get("member") else None
        )

class MentionedChannel:
    def __init__(self, data: dict):
        self.id: str = data.get("id")
        self.guild_id: str = data.get("guild_id")
        self.type: int = data.get("type")
        self.name: str = data.get("name")
from typing import (
    Optional
)
from .channels import GuildStageChannel, GuildChannel
from .guild import GuildScheduledEvent
from .application import Application
from .user import User
from .partials import PartialGuild

class Invite:
    def __init__(self, data: dict):
        self.code: str = data["code"]
        self.guild: Optional[PartialGuild] = PartialGuild(data["guild"]) or None
        self.channel: GuildChannel = GuildChannel(data["channel"]) 
        self.inviter: Optional[User] = User(data["inviter"]) or None
        self.target_type: int = data["target_type"]
        self.target_user: Optional[User] = User(data["target_user"]) or None
        self.target_application: Optional[Application] = Application(data["target_application"]) or None
        self.approximate_presence_count: Optional[int] = data["approximate_presence_count"] or None
        self.approximate_member_count: Optional[int] = data["approximate_member_count"] or None
        self.expires_at: Optional[str] = data["expires_at"] or None
        self.stage_instance: Optional[GuildStageChannel] = GuildStageChannel(data["stage_instance"]) or None
        self.guild_scheduled_event: Optional[GuildScheduledEvent] = GuildScheduledEvent(data["guild_scheduled_event"]) or None
    # Dabmaster is gonna work on this
    
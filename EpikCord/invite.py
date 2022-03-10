from .application import Application
from .channel import GuildChannel, GuildStageChannel
from .guild import PartialGuild, GuildScheduledEvent
from .member import User
from typing import Optional

class Invite:
    def __init__(self, data: dict):
        self.code: str = data.get("code")
        self.guild: Optional[PartialGuild] = PartialGuild(
            data.get("guild")) if data.get("guild") else None
        self.channel: GuildChannel = GuildChannel(
            data.get("channel")) if data.get("channel") else None
        self.inviter: Optional[User] = User(
            data.get("inviter")) if data.get("inviter") else None
        self.target_type: int = data.get("target_type")
        self.target_user: Optional[User] = User(
            data.get("target_user")) if data.get("target_user") else None
        self.target_application: Optional[Application] = Application(
            data.get("target_application")) if data.get("target_application") else None
        self.approximate_presence_count: Optional[int] = data.get(
            "approximate_presence_count")
        self.approximate_member_count: Optional[int] = data.get(
            "approximate_member_count")
        self.expires_at: Optional[str] = data.get("expires_at")
        self.stage_instance: Optional[GuildStageChannel] = GuildStageChannel(
            data.get("stage_instance")) if data.get("stage_instance") else None
        self.guild_scheduled_event: Optional[GuildScheduledEvent] = GuildScheduledEvent(
            data.get("guild_scheduled_event"))


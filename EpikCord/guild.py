from typing import (
    Optional
)
from .channels import GuildChannel, Thread
from .emoji import Emoji
from .user import User
from .member import Member
from .client import Client
from .role import Role
from typing import (
    List
)

class Guild:
    def __init__(self, client: Client, data: dict):
        self.client = client
        self.data: dict = data
        self.id: str = data["id"]
        self.name: str = data["name"]
        self.icon: Optional[str] = data["icon"] or None
        self.icon_hash: Optional[str] = data["icon_hash"] or None
        self.splash: Optional[str] = data["splash"] or None
        self.discovery_splash: Optional[str] = data["discovery_splash"] or None
        self.owner_id: str = data["owner_id"]
        self.permissions: str = data["permissions"]
        self.afk_channel_id: str = data["afk_channel_id"]
        self.afk_timeout: int = data["afk_timeout"]
        self.verification_level: str = "NONE" if data["verification_level"] == 0 else "LOW" if data["verification_level"] == 1 else "MEDIUM" if data["verification_level"] == 2 else "HIGH" if data["verification_level"] == 3 else "VERY_HIGH"
        self.default_message_notifications: str = "ALL" if data["default_message_notifications"] == 0 else "MENTIONS" 
        self.explicit_content_filter: str = "DISABLED" if data["explicit_content_filter"] == 0 else "MEMBERS_WITHOUT_ROLES" if data["explicit_content_filter"] == 1 else "ALL_MEMBERS"
        self.roles: List[Role] = [Role(role) for role in data["roles"]]
        self.emojis: List[Emoji] = [Emoji(emoji) for emoji in data["emojis"]]
        self.features: List[str] = data["features"]
        self.mfa_level: str = "NONE" if data["mfa_level"] == 0 else "ELEVATED"
        self.application_id: Optional[str] = data["application_id"] or None
        self.system_channel_id: Optional[str] = data["system_channel_id"] or None
        self.system_channel_flags: int = data["system_channel_flags"]
        self.rules_channel_id: Optional[int] = data["rules_channel_id"] or None
        self.joined_at: Optional[str] = data["joined_at"] or None
        self.large: bool = data["large"]
        self.unavailable: bool = data["unavailable"]
        self.member_count: int = data["member_count"]
        # self.voice_states: List[dict] = data["voice_states"]
        self.members: List[Member] = [Member(member) for member in data["members"]]
        self.channels: List[GuildChannel] = [GuildChannel(channel) for channel in data["channels"]]
        self.threads: List[Thread] = [Thread(thread) for thread in data["threads"]]
        self.presences: List[dict] = data["presences"]
        self.max_presences: int = data["max_presences"]
        self.max_members: int = data["max_members"]
        self.features
        
class GuildScheduledEvent:
    def __init__(self, client: Client, data: dict):
        self.id: str = data["id"]
        self.client = client
        self.guild_id: str = data["guild_id"]
        self.channel_id: Optional[str] = data["channel_id"] or None
        self.creator_id: Optional[str] = data["creator_id"] or None
        self.name: str = data["name"]
        self.description: Optional[str] = data["description"] or None
        self.scheduled_start_time: str = data["scheduled_start_time"]
        self.scheduled_end_time: Optional[str] = data["scheduled_end_time"] or None
        self.privacy_level: int = data["privacy_level"]
        self.status: str = "SCHEDULED" if data["status"] == 1 else "ACTIVE" if data["status"] == 2 else "COMPLETED" if data["status"] == 3 else "CANCELLED"
        self.entity_type: str = "STAGE_INSTANCE" if data["status"] == 1 else "VOICE" if data["status"] == 2 else "EXTERNAL"
        self.entity_id: str = data["entity_id"]
        self.entity_metadata: dict = data["entity_metadata"]
        self.creator: Optional[User] = User(data["creator"]) or None
        self.user_count: Optional[int] = data["user_count"] or None
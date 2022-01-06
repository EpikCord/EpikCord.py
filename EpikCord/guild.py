from typing import (
    Optional
)
from .user import User
from .client import ClientGuildMember, Client

class Guild:
    def __init__(self, client: Client, data: dict):
        self.member_cache: dict = {}
        self.client = client
        self.data: dict = data
        self.id: str = data["id"]
        self.name: str = data["name"]
        self.icon: Optional[str] = data["icon"] or None
        self.icon_hash: Optional[str] = data["icon_hash"] or None
        self.splash: Optional[str] = data["splash"] or None
        self.discovery_splash: Optional[str] = data["discovery_splash"] or None
        self.owner_id: str = data["owner_id"]
        self.me = ClientGuildMember(self.client)
        # self.me.permissions = data["permissions"]
        
        
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
from typing import (
    Optional
)

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
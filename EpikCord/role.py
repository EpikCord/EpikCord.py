from typing import (
    Optional,
    Union
)

class RoleTag:
    def __init__(self, data: dict):
        self.bot_id: Optional[str] = data["bot_id"] or None
        self.integration_id: Optional[str] = data["integration_id"] or None
        self.premium_subscriber: Optional[bool] = data["premium_subscriber"] or None
class Role:
    def __init__(self, client, data: dict):
        self.data = data
        self.client = client
        self.id: str = data["id"]
        self.name: str = data["name"]
        self.color: int = data["color"]
        self.hoist: bool = data["hoist"]
        self.icon: Optional[str] = data["icon"] or None
        self.unicode_emoji: Optional[str] = data["unicode_emoji"] or None
        self.position: int = data["position"]
        self.permissions: str = data["permissions"] # Permissions soon
        self.managed: bool = data["managed"]
        self.mentionable: bool = data["mentionable"]
        self.tags: RoleTag = RoleTag(self.data["tags"])
from typing import (
    Optional,
    List
)

class PartialUser:
    def __init__(self, data: dict):
        self.data: dict = data
        self.id: str = data["id"]
        self.username: str = data["username"]
        self.discriminator: str = data["discriminator"]
        self.avatar: Optional[str] = data["avatar"]

class PartialEmoji:
    def __init__(self, data):
        self.data: dict = data
        self.name: str = data["name"]
        self.id: str = data["id"]
        self.animated: bool = data["animated"]
    
class PartialGuild:
    def __init__(self, data):
        self.data: dict = data
        self.id: str = data["id"]
        self.name: str = data["name"]
        self.permissions: int = int(data["permissions"])
        self.features: List[str] = data["features"]
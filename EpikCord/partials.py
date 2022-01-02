from typing import (
    Optional
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
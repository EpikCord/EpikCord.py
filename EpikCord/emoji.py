from typing import (
    Optional,
    List
)
from .role import Role
from .user import User


class Emoji:
    def __init__(self, client, data: dict):
        self.id: Optional[str] = data["id"]
        self.name: Optional[str] = data["name"]
        self.roles: List[Role] = [Role(role) for role in data["roles"]]
        self.user: Optional[User] = User(data["user"]) if "user" in data else None
        self.requires_colons: bool = data["require_colons"]
        self.managed: bool = data["managed"]
        self.animated: bool = data["animated"]
        self.available: bool = data["available"]
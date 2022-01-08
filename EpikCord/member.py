from .client import Client
from .role import Role
from typing import (
    Optional,
    List
)
from .user import User

class ThreadMember:
    def __init__(self, data: dict):
        self.thread_id: str = data["thread_id"]
        self.user_id: str = data["user_id"]
        self.join_timestamp: str = data["join_timestamp"]
        self.flags: int = data["flags"]
        
class GuildMember:
    def __init__(self, client: Client, data: dict):
        self.data = data
        self.client = client
        self.user: Optional[User] = User(data["user"]) or None
        self.nick: Optional[str] = data["nick"] or None
        self.avatar: Optional[str] = data["avatar"] or None
        self.roles: List[Role] = [Role(role) for role in data["roles"]]
        self.joined_at:str = data["joined_at"]
        self.premium_since: Optional[str] = data["premium_since"] or None
        self.deaf: bool = data["deaf"]
        self.mute: bool = data["mute"]
        self.pending: Optional[bool] = data["pending"] or None
        self.permissions: Optional[str] = data["permissions"] or None
        self.communication_disabled_until: Optional[str] = data["communication_disabled_until"] or None
        

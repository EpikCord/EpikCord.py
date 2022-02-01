from typing import ( 
    Optional
)
# from .user import User
from .partials import PartialGuild

class SourceChannel:
    def __init__(self, data: dict):
        self.id: str = data["id"]
        self.name: str = data["name"]

class Webhook: # Not used for making webhooks.
    def __init__(self, client, data: dict):
        self.id: str = data["id"]
        self.client = client
        self.type: int = "Incoming" if data["type"] == 1 else "Channel Follower" if data["type"] == 2 else "Application"
        self.guild_id: Optional[str] = data["guild_id"]
        self.channel_id: Optional[str] = data["channel_id"]
        self.user: Optional[WebhookUser] = WebhookUser(data["user"])
        self.name: Optional[str] = data["name"]
        self.avatar: Optional[str] = data["avatar"]
        self.token: str = data["token"]
        self.application_id: Optional[str] = data["application_id"]
        self.source_guild: Optional[PartialGuild] = PartialGuild(data["source_guild"])
        self.source_channel: Optional[SourceChannel] = SourceChannel(data["source_channel"]) or None
        self.url: Optional[str] = data["url"]

class WebhookUser:
    def __init__(self, data: dict):
        self.webhook_id: str = data["webhook_id"]
        self.username: str = data["username"]
        self.avatar: str = data["avatar"]
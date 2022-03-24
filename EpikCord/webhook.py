
from typing import Optional
from .user import * 
from .partials import *
class WebhookUser:
    def __init__(self, data: dict):
        self.webhook_id: str = data.get("webhook_id")
        self.username: str = data.get("username")
        self.avatar: str = data.get("avatar")


class Webhook:
    def __init__(self, client, data: dict = None):
        """
        Don't pass in data if you're making a webhook, the lib passes data to construct an already existing webhook
        """
        self.client = client
        self.data = data
        if data:
            self.id: str = data.get("id")
            self.type: str = "Incoming" if data.get(
                "type") == 1 else "Channel Follower" if data.get("type") == 2 else "Application"
            self.guild_id: Optional[str] = data.get("guild_id")
            self.channel_id: Optional[str] = data.get("channel_id")
            self.user: Optional[User] = User(client, data.get("user"))
            self.name: Optional[str] = data.get("name")
            self.avatar: Optional[str] = data.get("avatar")
            self.token: Optional[str] = data.get("token")
            self.application_id: Optional[str] = data.get("application_id")
            self.source_guild: Optional[PartialGuild] = PartialGuild(
                data.get("source_guild"))
            self.url: Optional[str] = data.get("url")
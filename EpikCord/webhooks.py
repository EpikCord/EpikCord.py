from typing import Optional

from .partials import PartialGuild


class WebhookUser:
    def __init__(self, data: dict):
        self.webhook_id: str = data["webhook_id"]
        self.username: str = data["username"]
        self.avatar: str = data["avatar"]


class SourceChannel:
    def __init__(self, data: dict):
        self.id: str = data["id"]
        self.name: str = data["name"]


class Webhook:  # Not used for making webhooks
    def __init__(self, client, data: dict):
        self.id: str = data["id"]
        self.client = client
        self.type: str = (
            "Incoming"
            if data.get("type") == 1
            else "Channel Follower"
            if data.get("type") == 2
            else "Application"
        )
        self.guild_id: Optional[str] = data.get("guild_id")
        self.channel_id: Optional[str] = data.get("channel_id")
        self.user: Optional[WebhookUser] = (
            WebhookUser(data["user"]) if data.get("user") else None
        )
        self.name: Optional[str] = data.get("name")
        self.avatar: Optional[str] = data.get("avatar")
        self.token: Optional[str] = data.get("token")
        self.application_id: Optional[str] = data.get("application_id")
        self.source_guild: Optional[PartialGuild] = (
            PartialGuild(data["source_guild"]) if data.get("source_guild") else None
        )
        self.source_channel: Optional[SourceChannel] = (
            SourceChannel(data["source_channel"])
            if data.get("source_channel")
            else None
        )
        self.url: Optional[str] = data.get("url")


__all__ = ("Webhook", "WebhookUser", "SourceChannel")

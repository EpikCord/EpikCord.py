from typing import Optional

from discord_typings import PartialChannelData, UserData, WebhookData
from typing_extensions import TypedDict

from .partials import PartialGuild


class WebhookUserData(TypedDict):
    webhook_id: int
    username: str
    avatar: Optional[str]


class WebhookUser:
    def __init__(self, data: UserData):
        self.webhook_id: Optional[int] = data.get("webhook_id")  # type: ignore
        self.username: str = data["username"]
        self.avatar: Optional[str] = data.get("avatar")


class SourceChannel:
    def __init__(self, data: PartialChannelData):
        self.id: int = int(data["id"])
        self.name: str = data["name"]


class Webhook:  # Not used for making webhooks
    def __init__(self, client, data: WebhookData):
        self.id: int = int(data["id"])
        self.client = client
        self.type: str = (
            "Incoming"
            if data.get("type") == 1
            else "Channel Follower"
            if data.get("type") == 2
            else "Application"
        )
        self.guild_id: Optional[int] = int(data["guild_id"]) if data.get("guild_id") else None  # type: ignore
        self.channel_id: Optional[int] = int(data["channel_id"]) if data.get("channel_id") else None  # type: ignore
        self.user: Optional[WebhookUser] = (
            WebhookUser(data["user"]) if data.get("user") else None
        )
        self.name: Optional[str] = data.get("name")
        self.avatar: Optional[str] = data.get("avatar")
        self.token: Optional[str] = data.get("token")
        self.application_id: Optional[int] = int(data["application_id"]) if data.get("application_id") else None  # type: ignore
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

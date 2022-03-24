from typing import Optional, Dict, List
from .message import *
from .file import File
class Messageable:
    def __init__(self, client, channel_id: str):
        self.id: str = channel_id
        self.client = client

    async def fetch_messages(self, *, around: Optional[str] = None, before: Optional[str] = None, after: Optional[str] = None, limit: Optional[int] = None) -> List[Message]:
        response = await self.client.http.get(f"channels/{self.id}/messages", params={"around": around, "before": before, "after": after, "limit": limit})
        data = await response.json()
        return [Message(self.client, message) for message in data]

    async def fetch_message(self, *, message_id: str) -> Message:
        response = await self.client.http.get(f"channels/{self.id}/messages/{message_id}")
        data = await response.json()
        return Message(self.client, data)

    async def send(self, content: Optional[str] = None, *, embeds: Optional[List[dict]] = None, components=None, tts: Optional[bool] = False, allowed_mentions=None, sticker_ids: Optional[List[str]] = None, attachments: List[File]=None, suppress_embeds: bool = False) -> Message:
        payload = {}

        if content:
            payload["content"] = content

        if embeds:
            payload["embeds"] = [embed.to_dict() for embed in embeds]

        if components:
            payload["components"] = [component.to_dict()
                                     for component in components]

        if tts:
            payload["tts"] = tts

        if allowed_mentions:
            payload["allowed_mentions"] = allowed_mentions.to_dict()

        if sticker_ids:
            payload["sticker_ids"] = sticker_ids

        if attachments:
            payload["attachments"] = [attachment.to_dict()
                                      for attachment in attachments]

        if suppress_embeds:
            payload["suppress_embeds"] = 1 << 2

        response = await self.client.http.post(f"channels/{self.id}/messages", json=payload)
        data = await response.json()
        return Message(self.client, data)


class User(Messageable):
    def __init__(self, client, data: dict):
        super().__init__(client, data["id"])
        self.data = data
        self.client = client
        self.id: str = data.get("id")
        self.username: str = data.get("username")
        self.discriminator: str = data.get("discriminator")
        self.avatar: Optional[str] = data.get("avatar")
        self.bot: Optional[bool] = data.get("bot")
        self.system: Optional[bool] = data.get("system")
        self.mfa_enabled: bool = data.get("mfa_enabled")
        self.banner: Optional[str] = data.get("banner")
        # the user's banner color encoded as an integer representation of hexadecimal color code
        self.accent_color: Optional[int] = data.get("accent_color")
        self.locale: Optional[str] = data.get("locale")
        self.verified: bool = data.get("verified")
        self.email: Optional[str] = data.get("email")
        self.flags: int = data.get("flags")
        self.premium_type: int = data.get("premium_type")
        self.public_flags: int = data.get("public_flags")
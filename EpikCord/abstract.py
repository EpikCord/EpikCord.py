from __future__ import annotations
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from EpikCord import Message, File

class Messageable:
    def __init__(self, client, channel_id: str):
        self.id: str = channel_id
        self.client = client

    async def fetch_messages(
        self,
        *,
        around: Optional[str] = None,
        before: Optional[str] = None,
        after: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> List[Message]:
        from EpikCord import Message

        response = await self.client.http.get(
            f"channels/{self.id}/messages",
            params={"around": around, "before": before, "after": after, "limit": limit},
        )
        data = await response.json()
        return [Message(self.client, message) for message in data]

    async def fetch_message(self, *, message_id: str) -> Message:
        from EpikCord import Message

        response = await self.client.http.get(
            f"channels/{self.id}/messages/{message_id}"
        )
        data = await response.json()
        return Message(self.client, data)

    async def send(
        self,
        content: Optional[str] = None,
        *,
        embeds: Optional[List[dict]] = None,
        components=None,
        tts: Optional[bool] = False,
        allowed_mentions=None,
        sticker_ids: Optional[List[str]] = None,
        attachments: List[File] = None,
        suppress_embeds: bool = False,
    ) -> Message:
        from EpikCord import Message

        payload = {}

        if content:
            payload["content"] = content

        if embeds:
            payload["embeds"] = [embed.to_dict() for embed in embeds]

        if components:
            payload["components"] = [component.to_dict() for component in components]

        if tts:
            payload["tts"] = tts

        if allowed_mentions:
            payload["allowed_mentions"] = allowed_mentions.to_dict()

        if sticker_ids:
            payload["sticker_ids"] = sticker_ids

        if attachments:
            payload["attachments"] = [
                attachment.to_dict() for attachment in attachments
            ]

        if suppress_embeds:
            payload["suppress_embeds"] = 1 << 2

        response = await self.client.http.post(
            f"channels/{self.id}/messages", json=payload
        )
        data = await response.json()
        return Message(self.client, data)
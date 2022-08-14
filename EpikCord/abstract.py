from __future__ import annotations
import asyncio
from typing import Optional, List, TYPE_CHECKING
from .components import ActionRow
from abc import abstractmethod

if TYPE_CHECKING:
    from EpikCord import Message, File, AllowedMention, Check

class TypingContextManager:
    def __init__(self, client, channel_id):
        self.typing: asyncio.Task = None
        self.client = client
        self.channel_id: str = channel_id

    async def start_typing(self):

        await self.client.http.post(f"/channels/{self.channel_id}/typing")
        asyncio.get_event_loop().call_later(10, self.start_typing)

    async def __aenter__(self):
        self.typing = asyncio.create_task(self.start_typing())

    async def __aexit__(self):
        self.typing.cancel()

class Messageable:
    def __init__(self, client, channel_id: str):
        if isinstance(channel_id, (int, str)):
            self.id: str = channel_id
        elif isinstance(channel_id, dict):
            self.id: str = channel_id.get("id")
        else:
            raise TypeError(f"Expected str, int or dict, got {type(channel_id)}")

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
        components: List[ActionRow] = None,
        tts: Optional[bool] = False,
        allowed_mention: AllowedMention = None,
        sticker_ids: Optional[List[str]] = None,
        attachments: List[File] = None,
        suppress_embeds: bool = False,
    ) -> Message:
        from EpikCord import Message

        payload = self.client.utils.filter_values(
            {
                "content": content,
                "embeds": [embed.to_dict() for embed in embeds],
                "components": [component.to_dict() for component in components],
                "tts": tts,
                "allowed_mentions": allowed_mention.to_dict(),
                "sticker_ids": sticker_ids,
                "attachments": [attachment.to_dict() for attachment in attachments],
            }
        )

        if suppress_embeds:
            payload["suppress_embeds"] = 1 << 2

        response = await self.client.http.post(
            f"channels/{self.id}/messages", json=payload
        )
        data = await response.json()
        return Message(self.client, data)

    async def typing(self) -> TypingContextManager:
        return TypingContextManager(self.client, self.id)


class BaseCommand:
    def __init__(self, checks: Optional[List[Check]]):
        self.checks: List[Check] = checks

    def is_slash_command(self):
        return self.type == 1

    def is_user_command(self):
        return self.type == 2

    def is_message_command(self):
        return self.type == 3

    @property
    @abstractmethod
    def type(self):
        ...

class BaseChannel:
    def __init__(self, client, data: dict):
        self.id: str = data.get("id")
        self.client = client
        self.type = data.get("type")

__all__ = ("Messageable", "BaseCommand", "BaseChannel", "TypingContextManager")
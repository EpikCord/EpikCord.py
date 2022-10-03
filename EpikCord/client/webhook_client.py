from __future__ import annotations
from logging import getLogger
from typing import List, Optional
from EpikCord.components import Button, ActionRow, SelectMenu
from EpikCord.message import AllowedMention, Embed
from .http_client import HTTPClient

logger = getLogger(__name__)


class WebhookClient:
    def __init__(self):

        super().__init__()
        self.webhook_url = 'https://discord.com/api/v10/webhooks'

        async def execute( # main function
        self,
        webhook_id: int,
        webhook_token: str,
        username: Optional[str],
        avatar_url: Optional[str],
        tts: Optional[bool],
        embeds: Optional[List[Embed]],
        allowed_mentions: Optional[AllowedMention],
        content: Optional[str],
        components: Optional[List[ActionRow[Button, SelectMenu]]],
        ):

            self.http: HTTPClient = HTTPClient(
            )



__all__ = ("WebhookClient",)

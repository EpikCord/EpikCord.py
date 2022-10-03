from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Union

from ..utils import Utils
from .cache_manager import CacheManager

if TYPE_CHECKING:
    from ..channels import AnyChannel
    from ..client.client import Client, WebsocketClient


class ChannelManager(CacheManager):
    def __init__(self, client: Union[Client, WebsocketClient]):
        super().__init__()
        self.client = client

    async def fetch(self, channel_id: int) -> Optional[AnyChannel]:
        channel = await self.client.http.get(
            f"channels/{channel_id}", channel_id=channel_id
        )
        if data := await channel.json():
            return self.client.utils.channel_from_type(data)
        return None

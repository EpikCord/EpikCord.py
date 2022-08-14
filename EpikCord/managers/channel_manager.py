from typing import List, Optional, Union

from ..channels import (
    CategoryChannel,
    DMChannel,
    GuildChannel,
    GuildNewsChannel,
    GuildNewsThread,
    GuildStageChannel,
    GuildTextChannel,
    VoiceChannel,
)
from .cache_manager import CacheManager

AnyChannel = Union[
    GuildChannel,
    GuildTextChannel,
    GuildNewsChannel,
    VoiceChannel,
    DMChannel,
    CategoryChannel,
    GuildNewsThread,
    GuildStageChannel,
]


class ChannelManager(CacheManager):
    def __init__(self, client, channels: Optional[List[AnyChannel]] = None):
        super().__init__()
        self.client = client
        self.cache = {channel.id: channel for channel in channels} if channels else {}

    async def fetch(self, channel_id: str) -> Optional[AnyChannel]:
        channel = await self.client.http.get(
            f"channels/{channel_id}", channel_id=channel_id
        )
        if data := await channel.json():
            return self.client.utils.channel_from_type(data)
        return None

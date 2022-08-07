from typing import  Union, List, Optional

from .cache_manager import CacheManager
from .. import (
    GuildChannel,
    GuildTextChannel,
    GuildNewsChannel,
    VoiceChannel,
    DMChannel,
    ChannelCategory,
    GuildNewsThread,
    GuildStageChannel,
)

AnyChannel = Union[
    GuildChannel,
    GuildTextChannel,
    GuildNewsChannel,
    VoiceChannel,
    DMChannel,
    ChannelCategory,
    GuildNewsThread,
    GuildStageChannel,
]


class ChannelManager(CacheManager):
    def __init__(self, client, channels: Optional[List[AnyChannel]] = None, limit = 5000):
        super().__init__(limit)
        self.client = client
        self.cache = {channel.id: channel for channel in channels} if channels else {}

    async def fetch(self, channel_id: str) -> Optional[AnyChannel]:
        channel = await self.client.http.get(
            f"channels/{channel_id}", channel_id=channel_id
        )
        if data := await channel.json():
            return self.client.utils.channel_from_type(data)
        return None

from typing import (
    Union,
    List, 
    Optional
)
from .cache_manager import CacheManager
from ..channel import (
    TextBasedChannel, 
    GuildChannel, 
    GuildTextChannel, 
    GuildNewsChannel, 
    VoiceChannel, 
    DMChannel, 
    ChannelCategory, 
    GuildStoreChannel,
    GuildNewsThread, 
    GuildStageChannel
)

AnyChannel = Union[TextBasedChannel, GuildChannel, GuildTextChannel, GuildNewsChannel, VoiceChannel, DMChannel, ChannelCategory, GuildStoreChannel, GuildNewsThread, GuildStageChannel]

class ChannelManager(CacheManager):
    def __init__(self, client, channels: Optional[List[AnyChannel]] = None):
        self.channels = channels if channels is not None else []
    
    async def fetch(self, channel_id, *, skip_cache: Optional[bool] = False):
        if not skip_cache:
            for channel in self.channels:
                if channel.id == channel_id:
                    return channel

        channel = await self.client.http.get(f"channels/{channel_id}")

        self.channels.append(channel)
        return channel

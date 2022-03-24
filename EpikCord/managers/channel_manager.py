from typing import (
    Union,
    List,
    Optional
)
from .cache_manager import CacheManager
from ..__init__ import TextBasedChannel, GuildChannel, GuildTextChannel, GuildNewsChannel, VoiceChannel, DMChannel, ChannelCategory, GuildStoreChannel, GuildNewsThread, GuildStageChannel

AnyChannel = Union[TextBasedChannel, GuildChannel, GuildTextChannel, GuildNewsChannel, VoiceChannel, DMChannel, ChannelCategory, GuildStoreChannel, GuildNewsThread, GuildStageChannel]

class ChannelManager(CacheManager):
    def __init__(self, client, channels: Optional[List[AnyChannel]] = None):
        self.client = client
        self.channels = [client.utils.channel_from_type(channel_data) for channel_data in channels] if channels else []
    
    async def fetch(self, channel_id, *, skip_cache: Optional[bool] = False):
        if not skip_cache:
            filtered_list = list(filter(lambda channel: channel.id == channel_id, self.channels))
            if len(filtered_list) > 0:
                return filtered_list[0]

        channel_data = await self.client.http.get(f"channels/{channel_id}")

        channel = self.client.utils.channel_from_type(channel_data)

        self.channels.append(channel)
        return channel
from typing import (
    Union,
    List,
    Optional
)

from .cache_manager import CacheManager
from ..__init__ import GuildChannel, GuildTextChannel, GuildNewsChannel, VoiceChannel, DMChannel, ChannelCategory, \
    GuildNewsThread, GuildStageChannel

AnyChannel = Union[GuildChannel, GuildTextChannel, GuildNewsChannel, VoiceChannel, DMChannel, ChannelCategory, GuildNewsThread, GuildStageChannel]

class ChannelManager(CacheManager):
    def __init__(self, client, channels: Optional[List[AnyChannel]] = None):
        super().__init__("channels_cache")
        self.client = client
        self.channels = [client.utils.channel_from_type(channel_data) for channel_data in channels] if channels else []
    
    def format_cache(self):
        for channel in self.channels:
            self.channels_cache[channel.id] = channel
        return self.channels_cache

    async def fetch(self, channel_id, *, skip_cache: Optional[bool] = False):
        if not skip_cache:
            if filtered_list := list(
                filter(lambda channel: channel.id == channel_id, self.channels)
            ):
                return filtered_list[0]

        channel_data = await self.client.http.get(f"channels/{channel_id}")

        channel = self.client.utils.channel_from_type(channel_data)

        self.channels.append(channel)
        return channel
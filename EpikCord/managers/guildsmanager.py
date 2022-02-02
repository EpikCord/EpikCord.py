from typing import (
    List,
    Union
)
from .cachemanager import CacheManager
from ..__init__ import Guild, UnavailableGuild


class GuildManager(CacheManager):
    def __init__(self, guilds: List[Union[Guild,UnavailableGuild]]):
        for guild in guilds:
            self.cache[guild.id] = guild
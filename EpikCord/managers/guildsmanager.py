from typing import (
    List,
    Union
)
from .cachemanager import CacheManager
from ..guild import Guild, UnavailableGuild


class GuildManager(CacheManager):
    def __init__(self, guilds: List[Union[Guild,UnavailableGuild]]):
        for guild in guilds:
            self.cache[guild.id] = guild
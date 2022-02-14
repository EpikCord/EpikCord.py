from typing import (
    List,
    Union,
    Optional
)
from .cachemanager import CacheManager
from ..__init__ import Guild, UnavailableGuild


class GuildManager(CacheManager):
    def __init__(self, guilds: Optional[List[Union[Guild, UnavailableGuild]]] = []):
        for guild in guilds:
            self.cache[guild.id] = guild
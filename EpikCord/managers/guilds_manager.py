from typing import (
    List,
    Union,
    Optional
)
from .cachemanager import CacheManager
from ..__init__ import Guild, UnavailableGuild


class GuildManager(CacheManager):
    def __init__(self, client, guilds: Optional[List[Union[Guild, UnavailableGuild]]] = []):
        super().__init__()
        self.client = client
        for guild in guilds:
            self.cache[guild.id] = guild

    async def fetch(self, guild_id: str, *, skip_cache: Optional[bool] = False, with_counts: Optional[bool] = False):

        if guild_id in self.cache and not skip_cache:
            return self.cache[guild_id]

        if with_counts:
            return Guild(self.client, await self.client.http.get(f"/guilds/{guild_id}?with_counts=true"))
        return Guild(self.client, await self.client.http.get(f"/guilds/{guild_id}"))
        # TODO: This might not work...
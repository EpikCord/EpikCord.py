from typing import (
    List,
    Union,
    Optional
)

from .cache_manager import CacheManager
from ..__init__ import Guild, UnavailableGuild


class GuildManager(CacheManager):
    def __init__(self, client, guilds: Optional[List[Union[Guild, UnavailableGuild]]] = []):
        super().__init__("guilds_cache")
        self.client = client
        self.available_guilds = [guild for guild in guilds if not isinstance(guild, UnavailableGuild)]
        self.unavailable_guilds = [guild for guild in guilds if isinstance(guild, UnavailableGuild)]
        self.guilds = guilds

    def format_cache(self):
        for guild in self.guilds:
            self.guilds_cache[guild.id] = guild
        return self.guilds_cache

    async def fetch(self, guild_id: str, *, skip_cache: Optional[bool] = False, with_counts: Optional[bool] = False):

        if guild_id in self.cache and not skip_cache:
            return self.cache[guild_id]

        if with_counts:
            return Guild(self.client, await self.client.http.get(f"/guilds/{guild_id}?with_counts=true"))
        return Guild(self.client, await self.client.http.get(f"/guilds/{guild_id}"))
        # TODO: This might not work...
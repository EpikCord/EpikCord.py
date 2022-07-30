from typing import List, Union, Optional

from .cache_manager import CacheManager
from ..core import Guild, UnavailableGuild


class GuildManager(CacheManager):
    def __init__(
        self, client, guilds: Optional[List[Union[Guild, UnavailableGuild]]] = None
    ):
        if guilds is None:
            guilds = []

        super().__init__()
        self.client = client
        self.available_guilds = {
            guild.id: guild
            for guild in guilds
            if not isinstance(guild, UnavailableGuild)
        }
        self.unavailable_guilds = {
            guild.id: guild for guild in guilds if isinstance(guild, UnavailableGuild)
        }
        self.cache = {**self.available_guilds, **self.unavailable_guilds}

    async def fetch(
        self,
        guild_id: str,
        *,
        with_counts: Optional[bool] = False,
    ):

        if with_counts:
            return Guild(
                self.client,
                await self.client.http.get(f"/guilds/{guild_id}?with_counts=true"),
            )

        return Guild(self.client, await self.client.http.get(f"/guilds/{guild_id}"))

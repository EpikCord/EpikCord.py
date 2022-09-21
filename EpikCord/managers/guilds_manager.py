from __future__ import annotations

from typing import List, Optional, Union

from .cache_manager import CacheManager


class GuildManager(CacheManager):
    def __init__(self, client, guilds=None):
        if guilds is None:
            guilds = []

        from EpikCord import Guild, UnavailableGuild

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
        from EpikCord import Guild

        if with_counts:
            return Guild(
                self.client,
                await self.client.http.get(f"/guilds/{guild_id}?with_counts=true"),
            )

        return Guild(self.client, await self.client.http.get(f"/guilds/{guild_id}"))

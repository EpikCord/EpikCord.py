from __future__ import annotations

from typing import List, Optional, Union

from .cache_manager import CacheManager


class GuildManager(CacheManager):
    def __init__(self, client):
        super().__init__()
        self.client = client

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

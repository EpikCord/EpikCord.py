from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..client.client import Client 

from .cache_manager import CacheManager


class MemberManager(CacheManager):
    def __init__(self, client: Client, guild_id: int):
        super().__init__()
        self.client = client
        self.guild_id: int = guild_id
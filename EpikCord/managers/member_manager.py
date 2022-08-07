from typing import Optional

from .cache_manager import CacheManager


class MemberManager(CacheManager):
    def __init__(
        self, client, guild_id: str, members: Optional[list] = None, limit = 1000
    ):  # Will cause circular import
        if members is None:
            members = []

        super().__init__(limit)
        self.guild_id: str = guild_id
        for member in members:
            self.cache[member.id] = member

        self.client = client

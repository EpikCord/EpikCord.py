from typing import Optional

from .cache_manager import CacheManager


class MemberManager(CacheManager):
    def __init__(self, client, guild_id: str, members: Optional[list] = []): # Will cause circular import
        super().__init__("members")
        self.guild_id: str = guild_id
        for member in members:
            self.members[member.id] = member
        
        self.client = client

    async def fetch(self, member_id: str, *, skip_cache: bool = False):
        if self.members.get(member_id) is None or skip_cache:
            self.members[member_id] = await self.client.request_guild_members(self.guild_id, [member_id])
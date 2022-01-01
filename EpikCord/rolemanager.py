from .abc import Base
from .guild import Guild
from typing import List

class RoleManager(Base):
    def __init__(self, guild: Guild, roles: List[dict]):
        self.roles = guild.roles
    
    async def add(self, role_data: dict):
        response = await self.guild.client.http.post(f"guilds/{self.guild.id}/roles", data=role_data) # Send it to the server
        await self.roles.append(role_data) # Store it locally
        
    
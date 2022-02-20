from ..__init__ import Guild
from typing import List

class RoleManager:
    def __init__(self, guild: Guild):
        self.roles = guild.roles
    
    async def add(self, role_data: dict):
        response = await self.guild.client.http.post(f"guilds/{self.guild.id}/roles", data=role_data) # Send it to the server
        await self.roles.append(role_data) # Store it locally
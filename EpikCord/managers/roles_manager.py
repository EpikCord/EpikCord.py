from ..__init__ import Guild
from typing import List

class RoleManager:
    def __init__(self, guild: Guild):
        self.guild = guild
        self.roles = guild.roles
    async def add(self, role_data: dict):
        response = await self.guild.client.http.post(f"guilds/{self.guild.id}/roles", data=role_data) # Send it to the server
        await self.roles.append(role_data) # Store it locally
    
    async def delete(self,role_id:int):
        response = await self.guild.client.http.delete(f"guilds/{self.guild.id}/roles/{role_id}")
        #Todd: pop the local roles

    async def edit_role_pos(self,data:dict):
        response = await self.guild.client.http.patch(f"guilds/{self.guild.id}/roles", data=data)

    async def edit_role(self,role_id:str,data:dict):
        response= await self.guild.client.http.patch(f"guilds/{self.guild.id}/roles/{role_id}", data=data)
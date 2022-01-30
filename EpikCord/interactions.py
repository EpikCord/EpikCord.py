from typing import (
    Optional
    )

from .user import User
from .member import GuildMember

class BaseInteraction:
    def __init__(self, client, data: dict):
        self.id: str = data["id"]
        self.client = client
        self.application_id: int = data["application_id"]
        self.type: int = data["type"]
        self.data: Optional[dict] = data["data"] or None
        self.guild_id: Optional[str] = data["guild_id"] or None
        self.channel_id: Optional[str] = data["channel_id"] or None
        self.member: Optional[GuildMember] = GuildMember(data["member"]) or None
        self.user: Optional[User] = User(data["user"]) or None
        self.token: str = data["token"]
        self.version: int = data["version"]
        self.locale: Optional[str] = data["locale"] or None
        self.guild_locale: Optional[str] = data["guild_locale"] or None
        
    def is_ping(self):
        return self.type == 1
    
    def is_application_command(self):
        return self.type == 2
    
    def is_message_component(self):
        return self.type == 3
    
    def is_autocomplete(self):
        return self.type == 4
    
    async def reply(self, message_data: dict):
        response = await self.client.http.post(f"/interactions/{self.id}/{self.token}/callback", data=message_data)
        return await response.json()
    
    async def fetch_reply(self):
        response = await self.client.http.get(f"/webhooks/{self.application_id}/{self.token}/{self.token}/messages/@original")
        return await response.json()
    
    async def edit_reply(self, message_data: dict):
        response = await self.client.http.patch(f"/webhooks/{self.application_id}/{self.token}/messages/@original", data=message_data)
        return await response.json()
    
    async def delete_reply(self):
        response = await self.client.http.delete(f"/webhooks/{self.application_id}/{self.token}/messages/@original")
        return await response.json()
    
    async def followup(self, message_data: dict):
        response = await self.client.http.post(f"/webhooks/{self.application_id}/{self.token}", data=message_data)
        return await response.json()
    
    async def fetch_followup_message(self, message_id: str):
        response = await self.client.http.get(f"/webhooks/{self.application_id}/{self.token}/messages/{message_id}")
        return await response.json()
    
    async def edit_followup(self, message_id: str, message_data):
        response = await self.client.http.patch(f"/webhooks/{self.application_id}/{self.token}/messages/{message_id}", data=message_data)
        return await response.json()
    
    async def delete_followup(self, message_id: str):
        response = await self.client.http.delete(f"/webhooks/{self.application_id}/{self.token}/messages/{message_id}")
        return await response.json()
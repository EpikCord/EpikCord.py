from typing import (
    List,
    Optional
)
# from .client import Client
from .user import User
from .message import Message
from .member import GuildMember
from .exceptions import (
    InvalidArgumentType,
    CustomIdIsTooBig
)

class Messageable:
    def __init__(self, client, channel_id: str):
        self.channel_id: str = channel_id
        self.client = client
        
    async def fetch_messages(self,*, around: Optional[str] = None, before: Optional[str] = None, after: Optional[str] = None, limit: Optional[int] = None) -> List[Message]:
        response = await self.client.http.get(f"channels/{self.id}/messages", params={"around": around, "before": before, "after": after, "limit": limit})
        data = await response.json()
        return [Message(message) for message in data]
    
    async def fetch_message(self,*, message_id: str) -> Message:
        response = await self.client.http.get(f"channels/{self.id}/messages/{message_id}")
        data = await response.json()
        return Message(data)

    async def send(self, message_data: dict) -> Message:
        response = await self.client.http.post(f"channels/{self.id}/messages", data=message_data)
        return Message(await response.json())

class BaseSlashCommandOption:
    def __init__(self, *, name: str, description: str, required: bool = False):
        self.settings = {
            "name": name,
            "description": description,
            "required": required
        }
        # People shouldn't use this class, this is just a base class for other options
    
class BaseChannel:
    def __init__(self, client, data: dict):
        self.id: str = data["id"]
        self.client = client
        self.type = data["type"]

class BaseComponent:
    def __init__(self):
        self.settings = {}

    def set_custom_id(self, custom_id: str):
        
        if not isinstance(custom_id, str):
            raise InvalidArgumentType("Custom Id must be a string.")
        
        elif len(custom_id) > 100:
            raise CustomIdIsTooBig("Custom Id must be 100 characters or less.")

        self.settings["custom_id"] = custom_id
        
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
        self.message: Optional[Message] = Message(data["message"]) or None
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
    
    async def fetch_followup_message(self, message_id: Message.id):
        response = await self.client.http.get(f"/webhooks/{self.application_id}/{self.token}/messages/{message_id}")
        return await response.json()
    
    async def edit_followup(self, message_id: Message.id, message_data):
        response = await self.client.http.patch(f"/webhooks/{self.application_id}/{self.token}/messages/{message_id}", data=message_data)
        return await response.json()
    
    async def delete_followup(self, message_id: Message.id):
        response = await self.client.http.delete(f"/webhooks/{self.application_id}/{self.token}/messages/{message_id}")
        return await response.json()
    
    
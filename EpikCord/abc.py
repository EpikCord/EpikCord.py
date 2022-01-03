from typing import (
    List
)
from .channels import TextBasedChannel
from .embed import Embed
from .client import Client
from .message import Message
from .exceptions import (
    InvalidArgumentType,
    CustomIdIsTooBig
)

class Messageable:
    def __init__(self, client: Client, channel_id: str):
        self.channel_id: str = channel_id
        self.client = client
        
    async def send(self, content: str, *, **kwargs) -> Message:
        
        response = await self.client.http.post(f"channels/{self.channel_id}/messages", data={"content": content})
        data = await response.json()
        return Message(data)
        
class BaseSlashCommandOption:
    def __init__(self, *, name: str, description: str, required: bool = False):
        self.name: str = name
        self.description: str = description
        self.required: bool = required
        # People shouldn't use this class, this is just a base class for other options

    def to_json(self):
        return {
            "name": self.name,
            "description": self.description,
            "required": self.required
        }
    
class BaseChannel:
    def __init__(self, data: dict):
        self.id: str = data["id"]
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
    def __init__(self, data: dict):
        self.application_id: str = data["application_id"]
        self.channel: TextBasedChannel = 
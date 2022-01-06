from typing import (
    List
)
from .channels import TextBasedChannel
from .abc import BaseChannel
from .ws import WebsocketClient
from asyncio import run
from .member import Member
from .user import User
from .application import Application
from .route import Route

from aiohttp import ClientSession


class Client(WebsocketClient):

    def __init__(self, token: str, intents: int = 0, **options):
        super().__init__(token, intents)
        
        self.channels: List[BaseChannel] = []
        
        self.options: dict = options
        self.global_slash_commands: bool = options.get("global_slash_commands", True)
        self.slash_command_guilds: List[str] = options.get("slash_command_guilds", [])

        self.http = ClientSession(headers = {"Authorization": f"Bot {token}"}, base_url="https://discord.com/api/v9/")
        self.api = Route
        self.application: Application = Application(self, self.user) # Processes whatever it can        

    async def get_channel(self, channel_id: str):
        try:
            if self.channels[channel_id]:
                return self.channels[channel_id]
        except KeyError:
            response = await self.http.get(f"channels/{channel_id}")
            data = await response.json()
            return TextBasedChannel(data)

# class ClientUser(User):
    
#     def __init__(self, client: Client, data: dict):
#         super().__init__(data)
    
#     async def fetch(self):
#         response = await self.client.http.get("users/@me")
#         data = await response.json()
#         super().__init__(data) # Reinitialse the class with the new data.
    
# class ClientGuildMember(Member):
#     def __init__(self, client: Client,data: dict):
#         super().__init__(data)
from typing import (
    List
)
from .section import Section
from .channels import TextBasedChannel
from .abc import BaseChannel
from .ws import WebsocketClient
from asyncio import run
from .member import Member
from .user import User
from .application import Application
from .route import Route
from .abc import Messageable
from aiohttp import ClientSession


class Client(WebsocketClient):

    def __init__(self, token: str, intents: int = 0, **options):
        super().__init__(token, intents)
        
        self.channels: List[Messageable] = []
        
        self.options: dict = options

        self.http = ClientSession(headers = {"Authorization": f"Bot {token}"}, base_url="https://discord.com/api/v9/")
        self.api = Route
        self.application: Application = Application(self, self.user) # Processes whatever it can        

    def add_section(self, section: Section):
        for name, command_object in section.commands:
            self.client.commands[name] = command_object

        for event_name, event_func in section.events:
            self.events[event_name.lower().replace("on_")] = event_func
        
        # Successfully extracted all the valuable stuff from the section        

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
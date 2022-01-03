from typing import (
    List
)
from .ws import WebsocketClient
from .guild import Guild
from .member import Member
from .user import User
from .application import Application
from .route import Route
from aiohttp import ClientSession


class Client(WebsocketClient):

    def __init__(self, token: str):
        self.http = ClientSession(headers = {"Authorization": f"Bot {token}"}, base_url="https://discord.com/api/v9/")
        self.api = Route
        self.application: Application = Application(self, self.user) # Processes whatever it can
        self.user: ClientUser = ClientUser({"id": str(self.application.id)})
        self.guilds: List[Guild] = []

class ClientUser(User):
    
    def __init__(self, client: Client, data: dict):
        super().__init__(data)
        self.client: Client = client
    
    async def fetch(self):
        response = await self.client.http.get("users/@me")
        data = await response.json()
        super().__init__(data) # Reinitialse the class with the new data.
    
class ClientGuildMember(Member):
    def __init__(self, client: Client,data: dict):
        super().__init__(data)
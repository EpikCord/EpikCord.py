from .user import User
from .application import Application
from .route import Route
from aiohttp import ClientSession, ClientResponse

class Client:
    def __init__(self, token: str):
        self.http = ClientSession(headers = {"Authorization": f"Bot {token}"}, base_url="https://discord.com/api/v9/")
        self.api = Route
        self.application = Application(self)
        
    async def fetch_application(self):
        response: ClientResponse = await self.api(self, "oauth2/applications/@me").request("GET")
        response: ClientResponse = await response.json()
        self.application = Application(response)
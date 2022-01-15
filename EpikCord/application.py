from .team import Team
from .partials import PartialUser
from aiohttp import ClientResponse
from typing import (
    Optional
)
from .client import Client

class Application:
    def __init__(self, client: Client, data: dict):
        self.id: str = data["id"]
        self.client: Client = client
        self.name: str = data["name"]
        self.icon: Optional[str] = data["icon"] or None
        self.description: str = data["description"]
        self.rpc_origins: Optional[list] = data["rpc_origins"] or None
        self.bot_public: bool = data["bot_public"]
        self.bot_require_code_grant: bool = data["bot_require_code_grant"]
        self.terms_of_service_url: Optional[str] = data["terms_of_service"] or None
        self.privacy_policy_url: Optional[str] = data["privacy_policy"] or None
        self.owner: PartialUser = PartialUser(data["user"])
        self.summary: str = data["summary"]
        self.verify_key: str = data["verify_key"]
        self.team: Optional[Team] = Team(data["team"]) or None
        self.cover_image: Optional[str] = data["cover_image"] or None
        self.flags: int = data["flags"]

    async def fetch(self):
        response: ClientResponse = await self.client.api(self, "oauth2/applications/@me").request("GET")
        data: dict = await response.json()
        self.application = Application(data)
        
class ApplicationCommand:
    def __init__(self, data: dict):
        self.id: str = data["id"]
        self.type: int = data["type"]
        self.application_id: str = data["application_id"]
        self.guild_id: Optional[str] = data["guild_id"] or None
        self.name: str = data["name"]
        self.description: str = data["description"]
        self.default_permissions: bool = data["default_permissions"]
        self.version: str = data["version"]
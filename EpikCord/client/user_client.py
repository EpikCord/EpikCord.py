import datetime
from typing import Optional, List

from ..partials import PartialGuild
from ..application import Application
from ..type_enums import VisibilityType
from .http_client import HTTPClient
from ..user import User
from ..guild import Integration


class Connection:
    def __init__(self, data: dict):
        self.id: str = data["id"]
        self.name: str = data["name"]
        self.type: str = data["type"]
        self.revoked: Optional[bool] = data["revoked"]
        self.integrations: Optional[List[Integration]] = [
            Integration(data) for data in data.get("integrations", [])
        ]
        self.verified: bool = data["verified"]
        self.friend_sync: bool = data["friend_sync"]
        self.show_activity: bool = data["show_activity"]
        self.visibility: VisibilityType = VisibilityType(data["visibility"])


class AuthorizationInformation:
    def __init__(self, data: dict):
        self.application: Application = Application(data["application"])
        self.scopes: List[str] = data["scopes"]
        self.expires: datetime.datetime = datetime.datetime.fromisoformat(
            data["expires"]
        )
        self.user: Optional[User] = (
            User(self, data["user"]) if data.get("user") else None
        )

    def to_dict(self) -> dict:
        payload = {
            "application": self.application.to_dict(),
            "scopes": self.scopes,
            "expires": self.expires.isoformat(),
        }
        if self.user:
            payload["user"] = self.user.to_dict()

        return payload


class UserClient:
    """This class is meant to be used with an Access Token. Not a User Account Token. This does not support Self Bots."""

    def __init__(self, token: str, *, discord_endpoint: str):
        self.token = token
        from EpikCord import __version__

        self._http: HTTPClient = HTTPClient(
            headers={
                "Authorization": f"Bearer {token}",
                "User-Agent": f"DiscordBot (https://github.com/EpikCord/EpikCord.py {__version__})",
            },
            discord_endpoint=discord_endpoint,
        )
        self.application: Optional[Application] = None

    async def fetch_application(self):
        application = Application(
            await (await self._http.get("/oauth2/applications/@me")).json()
        )
        self.application: Optional[Application] = application
        return application

    async def fetch_authorization_information(self):
        data = await (await self._http.get("/oauth2/@me")).json()
        if self.application:
            data["application"] = self.application.to_dict()
        return AuthorizationInformation(data)

    async def fetch_connections(self) -> List[Connection]:
        data = await (await self._http.get("/users/@me/connections")).json()
        return [Connection(d) for d in data]

    async def fetch_guilds(
        self,
        *,
        before: Optional[str] = None,
        after: Optional[str] = None,
        limit: int = 200,
    ) -> List[PartialGuild]:
        params = {"limit": limit}

        if before:
            params["before"] = before
        if after:
            params["after"] = after

        data = await (await self._http.get("/users/@me/guilds", params=params)).json()

        return [PartialGuild(d) for d in data]

from __future__ import annotations
import datetime
from typing import List, Optional, TYPE_CHECKING

from ..application import Application
from ..guild import Integration
from ..partials import PartialGuild
from ..type_enums import VisibilityType
from ..user import User
from .http_client import HTTPClient


if TYPE_CHECKING:
    import discord_typings

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
    def __init__(self, data: discord_typings.AuthorizationInformationData):
        self.application: Application = Application(data["application"])
        self.scopes: List[str] = data["scopes"]
        self.expires: datetime.datetime = datetime.datetime.fromisoformat(
            data["expires"]
        )
        self.user: Optional[User] = (
            User(self, data["user"]) if data.get("user") else None
        )

    def to_dict(self) -> discord_typings.AuthorizationInformationData:
        payload: discord_typings.AuthorizationInformationData = {
            "application": self.application.to_dict(),
            "scopes": self.scopes,
            "expires": self.expires.isoformat(),
        }
        if self.user:
            payload["user"] = self.user.to_dict()

        return payload


class UserClient:
    """
    This class is meant to be used with an Access Token.
    Not a User Account Token. This does not support Self Bots.
    """

    def __init__(self, token: str, *, discord_endpoint: str = "https://discord.com/api/v10"):
        self.token = token

        self._http: HTTPClient = HTTPClient(
            token,
            discord_endpoint=discord_endpoint,
        )
        self.application: Optional[Application] = None

    async def fetch_application(self) -> Application:
        application = Application(
            await (await self._http.get("/oauth2/applications/@me")).json()
        )
        self.application = application
        return application

    async def fetch_authorization_information(self) -> AuthorizationInformation:
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
        before: Optional[int] = None,
        after: Optional[int] = None,
        limit: int = 200,
    ) -> List[PartialGuild]:
        params = {"limit": limit}

        if before:
            params["before"] = before
        if after:
            params["after"] = after

        data = await self._http.get("/users/@me/guilds", params=params)
        guilds = await data.json()

        return [PartialGuild(d) for d in guilds]


__all__ = ("UserClient",)

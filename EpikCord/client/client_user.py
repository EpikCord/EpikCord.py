from __future__ import annotations

from logging import getLogger
from typing import TYPE_CHECKING, Optional, Union

from ..user import User

if TYPE_CHECKING:
    import discord_typings

    from .client import Client
    from .websocket_client import WebsocketClient

logger = getLogger(__name__)


class ClientUser(User):
    def __init__(
        self, client: Union[Client, WebsocketClient], data: discord_typings.UserData
    ):
        super().__init__(client, data)
        if not self.bot:  # if they're a user account
            logger.critical(
                "Self botting is against Discord ToS. You can get banned. "
            )
            exit(1)

    async def fetch(self):
        response = await self.client.http.get("users/@me")
        data = await response.json()
        return ClientUser(self.client, data)
        # Reinitialize the class with the new data.

    async def edit(
        self, *, username: Optional[str] = None, avatar: Optional[bytes] = None
    ):
        payload = {}
        if username:
            payload["username"] = username
        if avatar:
            payload["avatar"] = self.client.utils.bytes_to_base64_data(avatar)
        response = await self.client.http.patch("users/@me", json=payload)
        data: discord_typings.UserData = await response.json()
        return ClientUser(self.client, data)


__all__ = ("ClientUser",)

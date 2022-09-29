from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from .abstract import Messageable

if TYPE_CHECKING:
    import discord_typings


class User(Messageable):
    def __init__(self, client, data: discord_typings.UserData):
        super().__init__(client, int(data["id"]))
        self.data = data
        self.client = client
        self.id: int = int(data["id"])
        self.username: str = data["username"]
        self.discriminator: str = data["discriminator"]
        self.avatar: Optional[str] = data.get("avatar")
        self.bot: Optional[bool] = data.get("bot")
        self.system: Optional[bool] = data.get("system")
        self.mfa_enabled: bool = data["mfa_enabled"]
        self.banner: Optional[str] = data.get("banner")
        # * the user's banner color encoded as an integer representation of
        # * hexadecimal color code
        self.accent_color: Optional[int] = data.get("accent_color")
        self.locale: Optional[str] = data.get("locale")
        self.verified: bool = data["verified"]
        self.email: Optional[str] = data.get("email")  # type: ignore
        self.flags: int = data["flags"]
        self.premium_type: int = data["premium_type"]
        self.public_flags: int = data["public_flags"]

    def to_dict(self) -> discord_typings.UserData:
        return self.data


__all__ = ("User",)

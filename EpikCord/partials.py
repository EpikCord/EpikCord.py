from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, Union

from EpikCord.flags import Permissions

if TYPE_CHECKING:
    import discord_typings


class PartialEmoji:
    def __init__(self, data):
        self.data = data
        self.name: str = data["name"]
        self.id: str = data["id"]
        self.animated: Optional[bool] = data.get("animated")

    def to_dict(self):
        payload: discord_typings.EmojiData = {
            "id": self.id,
            "name": self.name,
        }

        if self.animated is not None:
            payload["animated"] = self.animated

        return payload

class PartialChannel:
    def __init__(self, data: discord_typings.PartialChannelData):
        self.data = data
        self.id: int = int(data["id"])
        self.type: int = data["type"]
        self.permissions: Optional[Permissions] = Permissions(int(data["permissions"])) if data.get("permissions") else None

class PartialUser:
    def __init__(
        self, data: discord_typings.UserData
    ):  # I can't find a PartialUser data type, doesn't exist?
        self.data = data
        self.id: int = int(data["id"])
        self.username: str = data["username"]
        self.discriminator: str = data["discriminator"]
        self.avatar: Optional[str] = data.get("avatar")


class PartialGuild:
    def __init__(
        self, data: Union[discord_typings.GuildData, discord_typings.PartialGuildData]
    ):
        self.data = data
        self.id: int = int(data["id"])
        self.name: str = data["name"]
        self.permissions: Optional[Permissions] = (
            Permissions(int(data["permissions"])) if data.get("permissions") else None
        )
        self.features: Optional[List[discord_typings.GuildFeaturesData]] = data.get(
            "features"
        )


__all__ = ("PartialEmoji", "PartialUser", "PartialGuild")

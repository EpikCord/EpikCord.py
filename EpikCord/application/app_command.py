from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

from ..flags import Permissions
from ..localizations import Locale, Localization
from ..options import *
from ..type_enums import ApplicationCommandPermissionType

if TYPE_CHECKING:
    import discord_typings


class ApplicationCommand:
    def __init__(self, data: discord_typings.ApplicationCommandData):
        self.id: int = int(data["id"])
        self.type: int = data["type"]
        self.application_id: int = int(data["application_id"])
        self.guild_id: Optional[int] = (
            int(data["guild_id"]) if data.get("guild_id") else None
        )
        self.name: str = data["name"]
        self.description: str = data["description"]
        conversion_type = {
            1: Subcommand,
            2: SubCommandGroup,
            3: StringOption,
            4: IntegerOption,
            5: BooleanOption,
            6: UserOption,
            7: ChannelOption,
            8: RoleOption,
            9: MentionableOption,
            10: NumberOption,
            11: AttachmentOption,
        }
        self.options: List[AnyOption] = [
            conversion_type[option["type"]] for option in data["options"]  # type: ignore
        ]
        self.default_member_permissions: Optional[Permissions] = Permissions(
            int(data["default_member_permissions"]) # type: ignore
        ) if data.get("default_member_permissions") else None
        self.version: int = int(data["version"])
        self.name_localizations: Optional[List[Localization]] = [Localization(Locale(k), v) for (k, v) in data["name_localizations"].items()] if data.get("name_localizations") else None  # type: ignore
        self.description_localizations: Optional[List[Localization]] = (
            [
                Localization(Locale(k), v) for k, v in data["description_localizations"].items()  # type: ignore
            ]
            if data.get("description_localizations")
            else None
        )
        self.name_localisations = self.name_localizations
        self.description_localisations = self.description_localizations


class ApplicationCommandPermission:
    def __init__(self, data: discord_typings.ApplicationCommandPermissionsData):
        self.id: int = int(data["id"])
        self.type: ApplicationCommandPermissionType = ApplicationCommandPermissionType(
            data["type"]
        )
        self.permission: bool = data["permission"]


class GuildApplicationCommandPermission:
    def __init__(self, data: discord_typings.GuildApplicationCommandPermissionData):
        self.id: int = int(data["id"])
        self.application_id: int = int(data["application_id"])
        self.guild_id: int = int(data["guild_id"])
        self.permissions: List[ApplicationCommandPermission] = [
            ApplicationCommandPermission(permissions)
            for permissions in data["permissions"]
        ]

    def to_dict(self):
        return {
            "id": self.id,
            "application_id": self.application_id,
            "guild_id": self.guild_id,
            "permissions": self.permissions.to_dict(),
        }


__all__ = (
    "ApplicationCommand",
    "GuildApplicationCommandPermission",
    "ApplicationCommandPermission",
)

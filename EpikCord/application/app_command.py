from typing import List, Optional
from ..type_enums import ApplicationCommandPermissionType
from ..options import *
from ..localizations import Localization


class ApplicationCommand:
    def __init__(self, data: dict):
        self.id: str = data["id"]
        self.type: int = data["type"]
        self.application_id: str = data["application_id"]
        self.guild_id: Optional[str] = data.get("guild_id")
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
            conversion_type[option["type"]] for option in data["options"]
        ]
        self.default_member_permissions: str = data.get("default_permissions")
        self.version: str = data.get("version")
        self.name_localizations: List[Localization] = data.get("name_localizations")
        self.description_localizations: List[Localization] = [
            Localization(k, v) for k, v in data.get("description_localizations").items()
        ]
        self.name_localisations = self.name_localizations
        self.description_localisations = self.description_localizations


class ApplicationCommandPermission:
    def __init__(self, data):
        self.id: str = data.get("id")
        self.type: ApplicationCommandPermissionType = ApplicationCommandPermissionType(
            data.get("type")
        )
        self.permission: bool = data.get("permission")


class GuildApplicationCommandPermission:
    def __init__(self, data: dict):
        self.id: str = data.get("id")
        self.application_id: str = data.get("application_id")
        self.guild_id: str = data.get("guild_id")
        self.permissions: ApplicationCommandPermission = ApplicationCommandPermission(
            data.get("permissions")
        )

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

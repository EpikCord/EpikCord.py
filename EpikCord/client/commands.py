from typing import List, Optional

from ..flags import Permissions
from ..locales import Localization
from ..utils import (
    ApplicationCommandType,
    AsyncFunction,
    localization_list_to_dict,
)


class BaseClientCommand:
    def __init__(
        self,
        name: str,
        # description: str,
        callback: AsyncFunction,
        *,
        guild_ids: List[int] = [],
        name_localizations: List[Localization] = [],
        # description_localizations: List[Localization] = [],
        type: ApplicationCommandType = ApplicationCommandType.CHAT_INPUT,
        guild_only: bool = False,
        default_member_permissions: Optional[Permissions] = None,
        nsfw: bool = False,
    ):
        self.name = name
        # self.description = description
        self.guild_ids = guild_ids
        self.callback = callback
        self.name_localizations = name_localizations
        # self.description_localizations = description_localizations
        self.type = type
        self.guild_only = guild_only
        self.default_member_permissions = default_member_permissions
        self.nsfw = nsfw

    def to_dict(self):
        payload = {
            "name": self.name,
            # "description": self.description,
            "type": self.type.value,
            "nsfw": self.nsfw,
        }

        if self.guild_ids:
            payload["guild_ids"] = self.guild_ids
        if self.default_member_permissions:
            payload[
                "default_member_permissions"
            ] = self.default_member_permissions.value
        if self.guild_only is not None:
            payload["dm_permission"] = not self.guild_only
        if name_localizations := localization_list_to_dict(
            self.name_localizations
        ):
            payload["name_localizations"] = name_localizations
        # if description_localizations := localization_list_to_dict(self.description_localizations):
        #     payload["description_localizations"] = description_localizations

        return payload


class ClientContextMenuCommand(BaseClientCommand):
    ...

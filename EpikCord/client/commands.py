from typing import Dict, List, Optional, Union

from ..flags import Permissions
from ..locales import Localization
from ..utils import (
    ApplicationCommandOptionType,
    ApplicationCommandType,
    AsyncFunction,
    ChannelType,
    localization_list_to_dict,
)


class BaseClientCommand:
    def __init__(
        self,
        name: str,
        callback: AsyncFunction,
        *,
        guild_ids: List[int] = [],
        name_localizations: List[Localization] = [],
        type: ApplicationCommandType = ApplicationCommandType.CHAT_INPUT,
        guild_only: Optional[bool] = None,
        default_member_permissions: Optional[Permissions] = None,
        nsfw: bool = False,
    ):
        self.name = name
        self.guild_ids = guild_ids
        self.callback = callback
        self.name_localizations = name_localizations
        self.type = type
        self.guild_only = (
            guild_only
            if guild_only is not None
            else False
            if not self.guild_ids
            else True
        )
        self.default_member_permissions = default_member_permissions
        self.nsfw = nsfw

        if self.guild_ids and not self.guild_only:
            raise ValueError(
                "Guild IDs cannot be set if the command is not set to guild only."
            )

    def to_dict(self):
        payload = {
            "name": self.name,
            "type": self.type.value,
            "nsfw": self.nsfw,
            "dm_permission": not self.guild_only,
        }

        if self.guild_ids:
            payload["guild_ids"] = self.guild_ids
        if self.default_member_permissions:
            payload[
                "default_member_permissions"
            ] = self.default_member_permissions.value
        if name_localizations := localization_list_to_dict(
            self.name_localizations
        ):
            payload["name_localizations"] = name_localizations

        return payload


class ClientContextMenuCommand(BaseClientCommand):
    ...


class ClientUserCommand(ClientContextMenuCommand):
    def __init__(
        self,
        name: str,
        callback: AsyncFunction,
        *,
        guild_ids: List[int] = [],
        name_localizations: List[Localization] = [],
        guild_only: Optional[bool] = None,
        default_member_permissions: Optional[Permissions] = None,
        nsfw: bool = False,
    ):
        super().__init__(
            name,
            callback,
            guild_ids=guild_ids,
            name_localizations=name_localizations,
            type=ApplicationCommandType.USER,
            guild_only=guild_only,
            default_member_permissions=default_member_permissions,
            nsfw=nsfw,
        )


class ClientMessageCommand(ClientContextMenuCommand):
    def __init__(
        self,
        name: str,
        callback: AsyncFunction,
        *,
        guild_ids: List[int] = [],
        name_localizations: List[Localization] = [],
        guild_only: Optional[bool] = None,
        default_member_permissions: Optional[Permissions] = None,
        nsfw: bool = False,
    ):
        super().__init__(
            name,
            callback,
            guild_ids=guild_ids,
            name_localizations=name_localizations,
            type=ApplicationCommandType.MESSAGE,
            guild_only=guild_only,
            default_member_permissions=default_member_permissions,
            nsfw=nsfw,
        )


class ApplicationCommandOptionChoice:
    def __init__(
        self,
        name: str,
        value: str,
        *,
        name_localizations: List[Localization] = [],
    ):
        self.name = name
        self.value = value
        self.name_localizations = name_localizations

    def to_dict(self):
        payload: Dict[str, Union[str, Dict[str, str]]] = {
            "name": self.name,
            "value": self.value,
        }

        if name_localizations := localization_list_to_dict(
            self.name_localizations
        ):
            payload["name_localizations"] = name_localizations

        return payload


class BaseApplicationCommandOption:
    def __init__(
        self,
        name: str,
        description: str,
        *,
        name_localizations: List[Localization] = [],
        description_localizations: List[Localization] = [],
        required: bool = False,
        type: ApplicationCommandOptionType,
    ):
        self.name = name
        self.description = description
        self.name_localizations = name_localizations
        self.description_localizations = description_localizations
        self.required = required
        self.type = type

    def to_dict(self):
        payload = {
            "name": self.name,
            "description": self.description,
            "required": self.required,
            "type": self.type.value,
        }

        if name_localizations := localization_list_to_dict(
            self.name_localizations
        ):
            payload["name_localizations"] = name_localizations

        if description_localizations := localization_list_to_dict(
            self.description_localizations
        ):
            payload["description_localizations"] = description_localizations

        return payload


class BaseStringNumberOption(BaseApplicationCommandOption):
    def __init__(
        self,
        name: str,
        description: str,
        *,
        name_localizations: List[Localization] = [],
        description_localizations: List[Localization] = [],
        required: bool = False,
        type: ApplicationCommandOptionType,
        choices: List[ApplicationCommandOptionChoice] = [],
        autocomplete: bool = False,
    ):
        super().__init__(
            name,
            description,
            name_localizations=name_localizations,
            description_localizations=description_localizations,
            required=required,
            type=type,
        )
        self.choices = choices
        self.autocomplete = autocomplete

    def to_dict(self):
        payload = super().to_dict()
        if self.choices:
            payload["choices"] = [choice.to_dict() for choice in self.choices]
        if self.autocomplete:
            payload["autocomplete"] = True
        return payload


class BaseIntegerNumberOption(BaseStringNumberOption):
    def __init__(
        self,
        name: str,
        description: str,
        *,
        name_localizations: List[Localization] = [],
        description_localizations: List[Localization] = [],
        required: bool = False,
        type: ApplicationCommandOptionType,
        choices: List[ApplicationCommandOptionChoice] = [],
        autocomplete: bool = False,
        min_value: Optional[int] = None,
        max_value: Optional[int] = None,
    ):
        super().__init__(
            name,
            description,
            name_localizations=name_localizations,
            description_localizations=description_localizations,
            required=required,
            type=type,
            choices=choices,
            autocomplete=autocomplete,
        )
        self.min_value = min_value
        self.max_value = max_value

    def to_dict(self):
        payload = super().to_dict()
        if self.min_value:
            payload["min_value"] = self.min_value
        if self.max_value:
            payload["max_value"] = self.max_value
        return payload


class IntegerOption(BaseIntegerNumberOption):
    def __init__(
        self,
        name: str,
        description: str,
        *,
        name_localizations: List[Localization] = [],
        description_localizations: List[Localization] = [],
        required: bool = False,
        choices: List[ApplicationCommandOptionChoice] = [],
        autocomplete: bool = False,
        min_value: Optional[int] = None,
        max_value: Optional[int] = None,
    ):
        super().__init__(
            name,
            description,
            name_localizations=name_localizations,
            description_localizations=description_localizations,
            required=required,
            type=ApplicationCommandOptionType.INTEGER,
            choices=choices,
            autocomplete=autocomplete,
            min_value=min_value,
            max_value=max_value,
        )


class NumberOption(BaseIntegerNumberOption):
    def __init__(
        self,
        name: str,
        description: str,
        *,
        name_localizations: List[Localization] = [],
        description_localizations: List[Localization] = [],
        required: bool = False,
        choices: List[ApplicationCommandOptionChoice] = [],
        autocomplete: bool = False,
        min_value: Optional[int] = None,
        max_value: Optional[int] = None,
    ):
        super().__init__(
            name,
            description,
            name_localizations=name_localizations,
            description_localizations=description_localizations,
            required=required,
            type=ApplicationCommandOptionType.NUMBER,
            choices=choices,
            autocomplete=autocomplete,
            min_value=min_value,
            max_value=max_value,
        )


class StringOption(BaseStringNumberOption):
    def __init__(
        self,
        name: str,
        description: str,
        *,
        name_localizations: List[Localization] = [],
        description_localizations: List[Localization] = [],
        required: bool = False,
        choices: List[ApplicationCommandOptionChoice] = [],
        autocomplete: bool = False,
        min_length: Optional[int] = None,
        max_length: Optional[int] = None,
    ):
        super().__init__(
            name,
            description,
            name_localizations=name_localizations,
            description_localizations=description_localizations,
            required=required,
            type=ApplicationCommandOptionType.STRING,
            choices=choices,
            autocomplete=autocomplete,
        )
        self.min_length = min_length
        self.max_length = max_length

    def to_dict(self):
        payload = super().to_dict()
        if self.min_length:
            payload["min_length"] = self.min_length
        if self.max_length:
            payload["max_length"] = self.max_length
        return payload


class BooleanOption(BaseApplicationCommandOption):
    def __init__(
        self,
        name: str,
        description: str,
        *,
        name_localizations: List[Localization] = [],
        description_localizations: List[Localization] = [],
        required: bool = False,
    ):
        super().__init__(
            name,
            description,
            name_localizations=name_localizations,
            description_localizations=description_localizations,
            required=required,
            type=ApplicationCommandOptionType.BOOLEAN,
        )


class UserOption(BaseApplicationCommandOption):
    def __init__(
        self,
        name: str,
        description: str,
        *,
        name_localizations: List[Localization] = [],
        description_localizations: List[Localization] = [],
        required: bool = False,
    ):
        super().__init__(
            name,
            description,
            name_localizations=name_localizations,
            description_localizations=description_localizations,
            required=required,
            type=ApplicationCommandOptionType.USER,
        )


class RoleOption(BaseApplicationCommandOption):
    def __init__(
        self,
        name: str,
        description: str,
        *,
        name_localizations: List[Localization] = [],
        description_localizations: List[Localization] = [],
        required: bool = False,
    ):
        super().__init__(
            name,
            description,
            name_localizations=name_localizations,
            description_localizations=description_localizations,
            required=required,
            type=ApplicationCommandOptionType.ROLE,
        )


class AttachmentOption(BaseApplicationCommandOption):
    def __init__(
        self,
        name: str,
        description: str,
        *,
        name_localizations: List[Localization] = [],
        description_localizations: List[Localization] = [],
        required: bool = False,
    ):
        super().__init__(
            name,
            description,
            name_localizations=name_localizations,
            description_localizations=description_localizations,
            required=required,
            type=ApplicationCommandOptionType.ATTACHMENT,
        )


class MentionableOption(BaseApplicationCommandOption):
    def __init__(
        self,
        name: str,
        description: str,
        *,
        name_localizations: List[Localization] = [],
        description_localizations: List[Localization] = [],
        required: bool = False,
    ):
        super().__init__(
            name,
            description,
            name_localizations=name_localizations,
            description_localizations=description_localizations,
            required=required,
            type=ApplicationCommandOptionType.MENTIONABLE,
        )


class ChannelOption(BaseApplicationCommandOption):
    def __init__(
        self,
        name: str,
        description: str,
        *,
        name_localizations: List[Localization] = [],
        description_localizations: List[Localization] = [],
        required: bool = False,
        channel_types: Optional[List[ChannelType]],
    ):
        super().__init__(
            name,
            description,
            name_localizations=name_localizations,
            description_localizations=description_localizations,
            required=required,
            type=ApplicationCommandOptionType.CHANNEL,
        )
        self.channel_types = channel_types

    def to_dict(self):
        payload = super().to_dict()
        if self.channel_types:
            payload["channel_types"] = self.channel_types
        return payload


ApplicationCommandOption = Union[
    IntegerOption,
    NumberOption,
    StringOption,
    BooleanOption,
    UserOption,
    RoleOption,
    AttachmentOption,
    MentionableOption,
    ChannelOption,
]


class ClientChatInputCommand(BaseClientCommand):
    def __init__(
        self,
        name: str,
        description: str,
        callback: AsyncFunction,
        *,
        guild_ids: List[int] = [],
        name_localizations: List[Localization] = [],
        description_localizations: List[Localization] = [],
        type: ApplicationCommandType = ApplicationCommandType.CHAT_INPUT,
        guild_only: Optional[bool] = None,
        default_member_permissions: Optional[Permissions] = None,
        nsfw: bool = False,
        options: Optional[List[str]] = None,
    ):
        super().__init__(
            name,
            callback,
            guild_ids=guild_ids,
            name_localizations=name_localizations,
            type=type,
            guild_only=guild_only,
            default_member_permissions=default_member_permissions,
            nsfw=nsfw,
        )
        self.description = description
        self.description_localizations = description_localizations
        self.options = options

    def to_dict(self):
        payload = super().to_dict()

        payload["description"] = self.description

        if description_localizations := localization_list_to_dict(
            self.description_localizations
        ):
            payload["description_localizations"] = description_localizations
        if self.options:
            payload["options"] = [option.to_dict() for option in self.options]  # type: ignore # I still need to create the Option class

        return payload

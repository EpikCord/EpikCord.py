from __future__ import annotations
from typing import Optional, Union, List
from .localizations import Localization
from .type_enums import ChannelTypes, Locale


class BaseSlashCommandOption:
    def __init__(self, *, name: str, description: str, required: Optional[bool] = True):
        self.name: str = name
        self.description: str = description
        self.required: bool = required
        self.type: Optional[int] = None  #! Needs to be set by the subclass
        #! People shouldn't use this class, this is just a base class for other
        #! options, but they can use this for other options we are yet to account for.

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "required": self.required,
            "type": self.type,
        }


class StringOption(BaseSlashCommandOption):
    def __init__(
        self,
        *,
        name: str,
        description: Optional[str] = None,
        required: bool = True,
        autocomplete: Optional[bool] = False,
        min_length: Optional[int] = None,
        max_length: Optional[int] = None,
    ):
        super().__init__(name=name, description=description, required=required)
        self.type = 3
        self.min_length = min_length
        self.max_length = max_length
        self.autocomplete = autocomplete

    def to_dict(self):
        usual_dict = super().to_dict()
        usual_dict["autocomplete"] = self.autocomplete

        if self.min_length:
            usual_dict["min_length"] = self.min_length
        if self.max_length:
            usual_dict["max_length"] = self.max_length

        return usual_dict


class IntegerOption(BaseSlashCommandOption):
    def __init__(
        self,
        *,
        name: str,
        description: Optional[str] = None,
        required: bool = True,
        autocomplete: Optional[bool] = False,
        min_value: Optional[int] = None,
        max_value: Optional[int] = None,
    ):
        super().__init__(name=name, description=description, required=required)
        self.type = 4
        self.autocomplete = autocomplete
        self.min_value = min_value
        self.max_value = max_value

    def to_dict(self):
        usual_dict = super().to_dict()
        usual_dict["autocomplete"] = self.autocomplete
        if self.min_value:
            usual_dict["min_value"] = self.min_value
        if self.max_value:
            usual_dict["max_value"] = self.max_value
        return usual_dict


class BooleanOption(BaseSlashCommandOption):
    def __init__(
        self, *, name: str, description: Optional[str] = None, required: bool = True
    ):
        super().__init__(name=name, description=description, required=required)
        self.type = 5


class UserOption(BaseSlashCommandOption):
    def __init__(
        self, *, name: str, description: Optional[str] = None, required: bool = True
    ):
        super().__init__(name=name, description=description, required=required)
        self.type = 6


class ChannelOption(BaseSlashCommandOption):
    def __init__(
        self, *, name: str, description: Optional[str] = None, required: bool = True
    ):
        super().__init__(name=name, description=description, required=required)
        self.type = 7
        self.channel_types: List[ChannelTypes] = []

    def to_dict(self):
        usual_dict: dict = super().to_dict()
        usual_dict["channel_types"] = self.channel_types
        return usual_dict


class RoleOption(BaseSlashCommandOption):
    def __init__(
        self, *, name: str, description: Optional[str] = None, required: bool = True
    ):
        super().__init__(name=name, description=description, required=required)
        self.type = 8


class MentionableOption(BaseSlashCommandOption):
    def __init__(
        self, *, name: str, description: Optional[str] = None, required: bool = True
    ):
        super().__init__(name=name, description=description, required=required)
        self.type = 9


class NumberOption(BaseSlashCommandOption):
    def __init__(
        self,
        *,
        name: str,
        description: Optional[str] = None,
        required: bool = True,
        autocomplete: Optional[bool] = False,
        min_value: Optional[int] = None,
        max_value: Optional[int] = None,
    ):
        super().__init__(name=name, description=description, required=required)
        self.type = 10
        self.autocomplete = autocomplete
        self.min_value = min_value
        self.max_value = max_value

    def to_dict(self):
        usual_dict = super().to_dict()
        usual_dict["autocomplete"] = self.autocomplete
        if self.min_value:
            usual_dict["min_value"] = self.min_value
        if self.max_value:
            usual_dict["max_value"] = self.max_value
        return usual_dict


class AttachmentOption(BaseSlashCommandOption):
    def __init__(
        self, *, name: str, description: Optional[str] = None, required: bool = True
    ):
        super().__init__(name=name, description=description, required=required)
        self.type = 11


class SlashCommandOptionChoice:
    def __init__(
        self,
        *,
        name: str,
        value: Union[float, int, str],
        name_localization: Optional[List[Localization]],
    ):
        self.name: str = name
        self.value: Union[float, int, str] = value
        self.name_localizations: List[Localization] = [
            Localization(k, v) for k, v in name_localization.items()
        ]
        self.name_localisations = self.name_localizations

    def to_dict(self):
        return {"name": self.name, "value": self.value}


class Subcommand(BaseSlashCommandOption):
    conversion_type = {
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

    def __init__(
        self,
        *,
        name: str,
        description: str = None,
        options: Optional[List[AnyOption]] = None,
    ):
        super().__init__(name=name, description=description)
        self.type = 1
        converted_options = []

        if not options:
            options = []

        for option in [option.to_dict() for option in options]:
            if option["type"] == 1:
                converted_options.append(StringOption(**option))

            elif option["type"] == 2:
                converted_options.append(SubCommandGroup(**option))

            else:
                option_type = option.pop("type", None)
                converted_options.append(self.conversion_type[option_type](**option))

        self.options: List[AnyOption] = converted_options

    def to_dict(self):
        usual_dict = super().to_dict()
        usual_dict.pop("required", None)
        usual_dict["options"] = [option.to_dict() for option in self.options]
        return usual_dict


class SubCommandGroup(BaseSlashCommandOption):
    conversion_type = {
        1: Subcommand,
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

    def __init__(
        self,
        *,
        name: str,
        description: str = None,
        options: Optional[List[AnyOption]] = None,
    ):
        super().__init__(name=name, description=description)
        self.type = 2
        converted_options = []
        for option in [option.to_dict() for option in options]:
            if option["type"] == 2:
                converted_options.append(SubCommandGroup(**option))
            else:
                option_type = option.pop("type", None)
                converted_options.append(self.conversion_type[option_type](**option))

        self.options: List[AnyOption] = converted_options

    def to_dict(self):
        usual_dict = super().to_dict()
        usual_dict.pop("required", None)
        usual_dict["options"] = [option.to_dict() for option in self.options]
        return usual_dict


AnyOption = Union[
    Subcommand,
    SubCommandGroup,
    StringOption,
    IntegerOption,
    BooleanOption,
    UserOption,
    ChannelOption,
    RoleOption,
    MentionableOption,
    NumberOption,
]

from .enums import ChannelOptionChannelTypes
from .exceptions import InvalidOption
from typing import Optional, Union

class BaseSlashCommandOption:
    def __init__(self, *, name: str, description: str, required: Optional[bool] = False):
        self.name: str = name
        self.description: str = description
        self.required: bool = required
        self.type: int = None # Needs to be set by the subclass
        # People shouldn't use this class, this is just a base class for other options, but they can use this for other options we are yet to account for.

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "required": self.required,
            "type": self.type
        }
    
class StringOption(BaseSlashCommandOption):
    def __init__(self, *, name: str, description: Optional[str] = None, required: bool = True, autocomplete: Optional[bool] = False):
        super().__init__(name=name, description=description, required=required)
        self.type = 3
        self.autocomplete = autocomplete

    def to_dict(self):
        usual_dict = super().to_dict()
        usual_dict["autocomplete"] = self.autocomplete
        return usual_dict


class IntegerOption(BaseSlashCommandOption):
    def __init__(self, *, name: str, description: Optional[str] = None, required: bool = True, autocomplete: Optional[bool] = False, min_value: Optional[int] = None, max_value: Optional[int] = None):
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
    def __init__(self, *, name: str, description: Optional[str] = None, required: bool = True):
        super().__init__(name=name, description=description, required=required)
        self.type = 5


class UserOption(BaseSlashCommandOption):
    def __init__(self, *, name: str, description: Optional[str] = None, required: bool = True):
        super().__init__(name=name, description=description, required=required)
        self.type = 6


class ChannelOption(BaseSlashCommandOption):
    def __init__(self, *, name: str, description: Optional[str] = None, required: bool = True):
        super().__init__(name=name, description=description, required=required)
        self.type = 7
        self.channel_types: list[ChannelOptionChannelTypes] = []
        
    def to_dict(self):
        usual_dict: dict = super().to_dict()
        usual_dict["channel_types"] = self.channel_types
        return usual_dict

class RoleOption(BaseSlashCommandOption):
    def __init__(self, *, name: str, description: Optional[str] = None, required: bool = True):
        super().__init__(name=name, description=description, required=required)
        self.type = 8


class MentionableOption(BaseSlashCommandOption):
    def __init__(self, *, name: str, description: Optional[str] = None, required: bool = True):
        super().__init__(name=name, description=description, required=required)
        self.type = 9


class NumberOption(BaseSlashCommandOption):
    def __init__(self, *, name: str, description: Optional[str] = None, required: bool = True, autocomplete: Optional[bool] = False, min_value: Optional[int] = None, max_value: Optional[int] = None):
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
    def __init__(self, *, name: str, description: Optional[str] = None, required: bool = True):
        super().__init__(name=name, description=description, required=required)
        self.type = 11


class SlashCommandOptionChoice:
    def __init__(self, * name: str, value: Union[float, int, str]):
        self.name: str = name
        self.value: Union[float, int, str] = value
    
    def to_dict(self):
        return {
            "name": self.name,
            "value": self.value
        }


class Subcommand(BaseSlashCommandOption):
    def __init__(self, *, name: str, description: str = None, required: bool = True, options: list[Union[StringOption, IntegerOption, BooleanOption, UserOption, ChannelOption, RoleOption, MentionableOption, NumberOption]] = None):
        super().__init__(name=name, description=description, required=required)
        self.type = 1
        converted_options = []
        for option in options:
            if option["type"] == 1:
                converted_options.append(Subcommand(**option))
            elif option["type"] == 2:
                raise InvalidOption("You can't have a subcommand group with a subcommand")
            elif option["type"] == 3:
                converted_options.append(StringOption(**option))
            elif option["type"] == 4:
                converted_options.append(IntegerOption(**option))
            elif option["type"] == 5:
                converted_options.append(BooleanOption(**option))
            elif option["type"] == 6:
                converted_options.append(UserOption(**option))
            elif option["type"] == 7:
                converted_options.append(ChannelOption(**option))
            elif option["type"] == 8:
                converted_options.append(RoleOption(**option))
            elif option["type"] == 9:
                converted_options.append(MentionableOption(**option))
            elif option["type"] == 10:
                converted_options.append(NumberOption(**option))
            elif option["type"] == 11:
                converted_options.append(AttachmentOption(**option))

        self.options: Union[Subcommand, SubCommandGroup, StringOption, IntegerOption, BooleanOption, UserOption, ChannelOption, RoleOption, MentionableOption, NumberOption] = converted_options




class SubCommandGroup(BaseSlashCommandOption):
    def __init__(self, *, name: str, description: str = None, required: bool = True, options: list[Union[Subcommand, StringOption, IntegerOption, BooleanOption, UserOption, ChannelOption, RoleOption, MentionableOption, NumberOption]] = None):
        super().__init__(name=name, description=description, required=required)
        self.type = 2
        converted_options = []
        for option in options:
            if option["type"] == 1:
                converted_options.append(Subcommand(**option))
            elif option["type"] == 2:
                converted_options.append(SubCommandGroup(**option))
            elif option["type"] == 3:
                converted_options.append(StringOption(**option))
            elif option["type"] == 4:
                converted_options.append(IntegerOption(**option))
            elif option["type"] == 5:
                converted_options.append(BooleanOption(**option))
            elif option["type"] == 6:
                converted_options.append(UserOption(**option))
            elif option["type"] == 7:
                converted_options.append(ChannelOption(**option))
            elif option["type"] == 8:
                converted_options.append(RoleOption(**option))
            elif option["type"] == 9:
                converted_options.append(MentionableOption(**option))
            elif option["type"] == 10:
                converted_options.append(NumberOption(**option))
            elif option["type"] == 11:
                converted_options.append(AttachmentOption(**option))

        self.options: Union[Subcommand, SubCommandGroup, StringOption, IntegerOption, BooleanOption, UserOption, ChannelOption, RoleOption, MentionableOption, NumberOption] = converted_options

    def to_dict(self):
        usual_dict = super().to_dict()
        payload_to_append = []
        for option in self.options:
            payload_to_append(option.to_dict())
        
        usual_dict["options"] = payload_to_append
        return usual_dict


AnyOption = Union[Subcommand, SubCommandGroup, StringOption, IntegerOption, BooleanOption, UserOption, ChannelOption, RoleOption, MentionableOption, NumberOption]

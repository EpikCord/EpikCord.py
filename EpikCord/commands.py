from .exceptions import InvalidOption
from typing import Optional, Union, List

class ChannelOptionChannelTypes:
    """
    An Enum for the channel types that can be used to restrict the channel types which can be chosen for a ChannelOption.
    """
    GUILD_TEXT = 0
    DM = 1
    GUILD_VOICE = 2
    GUILD_CATEGORY = 4
    GUILD_NEWS = 5
    GUILD_STORE = 6
    GUILD_NEWS_THREAD = 10
    GUILD_PUBLIC_THREAD = 11
    GUILD_PRIVATE_THREAD = 12
    GUILD_STAGE_VOICE = 13

class BaseSlashCommandOption:
    """
    The base SlashCommandOption class.
    Can be used for new options. that are yet to be created in EpikCord.

    Attributes
    ----------
    name: :class:`str`
        The name of the option.
    description: :class:`str`
        The description of the option.
    required: :class:`bool`
        Whether the option is required or not.

    Parameters
    ----------
    name: :class:`str`
        The name of the option.
    description: :class:`str`
        The description of the option.
    required: :class:`bool`
        Whether the option is required or not.
    """
    def __init__(self, *, name: str, description: str, required: Optional[bool] = False):
        self.name: str = name
        self.description: str = description
        self.required: bool = required or None
        self.type: int = None # Needs to be set by the subclass
        # People shouldn't use this class, this is just a base class for other options, but they can use this for other options we are yet to account for.

    def to_dict(self):
        """
        Returns a dictionary representation of the option.
        """
        payload = {
            "name": self.name,
            "description": self.description,
            "type": self.type
        }
        if self.required is not None:
            payload["required"] = self.required
        
        return payload
    
class StringOption(BaseSlashCommandOption):
    """
    The StringOption class.
    Used for options that are strings.

    Attributes
    ----------
    name: :class:`str`
        The name of the option.
    description: :class:`str`
        The description of the option.
    required: :class:`bool`
        Whether the option is required or not.
    autocomplete: :class:`bool`
        Whether the option should autocomplete or not.

    Parameters
    ----------
    name: :class:`str`
        The name of the option.
    description: :class:`str`
        The description of the option.
    required: :class:`bool`
        Whether the option is required or not.
    autocomplete: :class:`bool`
        Whether the option should autocomplete or not.
    """
    def __init__(self, *, name: str, description: Optional[str] = None, required: bool = True, autocomplete: Optional[bool] = False):
        super().__init__(name=name, description=description, required=required)
        self.type = 3
        self.autocomplete = autocomplete

    def to_dict(self):
        usual_dict = super().to_dict()
        usual_dict["autocomplete"] = self.autocomplete
        return usual_dict


class IntegerOption(BaseSlashCommandOption):
    """
    The IntegerOption class.
    Used for options that are integers (whole numbers).
   
    Attributes
    ----------
    name: :class:`str`
        The name of the option.
    description: :class:`str`
        The description of the option.
    required: :class:`bool`
        Whether the option is required or not.
    autocomplete: :class:`bool`
        Whether the option should autocomplete or not.
    min_value: :class:`int`
        The minimum value of the option.
    max_value: :class:`int`
        The maximum value of the option.

    Parameters
    ----------
    name: :class:`str`
        The name of the option.
    description: :class:`str`
        The description of the option.
    required: :class:`bool`
        Whether the option is required or not.
    autocomplete: :class:`bool`
        Whether the option should autocomplete or not.
    min_value: :class:`int`
        The minimum value of the option.
    max_value: :class:`int`
        The maximum value of the option.
    """
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
    """
    The BooleanOption class.
    Used for options that are booleans.

    Attributes
    ----------
    name: :class:`str`
        The name of the option.
    description: :class:`str`
        The description of the option.
    required: :class:`bool`
        Whether the option is required or not.

    Parameters
    ----------
    name: :class:`str`
        The name of the option.
    description: :class:`str`
        The description of the option.
    required: :class:`bool`
        Whether the option is required or not.
    """
    def __init__(self, *, name: str, description: Optional[str] = None, required: bool = True):
        super().__init__(name=name, description=description, required=required)
        self.type = 5


class UserOption(BaseSlashCommandOption):
    """
    The UserOption class.
    Used for options that are users.

    Attributes
    ----------
    name: :class:`str`
        The name of the option.
    description: :class:`str`
        The description of the option.
    required: :class:`bool`
        Whether the option is required or not.

    Parameters
    ----------
    name: :class:`str`
        The name of the option.
    description: :class:`str`
        The description of the option.
    required: :class:`bool`
        Whether the option is required or not.

    """
    def __init__(self, *, name: str, description: Optional[str] = None, required: bool = True):
        super().__init__(name=name, description=description, required=required)
        self.type = 6


class ChannelOption(BaseSlashCommandOption):
    """
    The ChannelOption class.
    Used for options that are channels.
    
    Attributes
    ----------
    name: :class:`str`
        The name of the option.
    description: :class:`str`
        The description of the option.
    required: :class:`bool`
        Whether the option is required or not.
    channel_types: :class:`list`
        The channel types that the option can be.

    Parameters
    ----------
    name: :class:`str`
        The name of the option.
    description: :class:`str`
        The description of the option.
    required: :class:`bool`
        Whether the option is required or not.
    channel_types: :class:`list`
        The channel types that the option can be.
    """

    def __init__(self, *, name: str, description: Optional[str] = None, required: bool = True, channel_types: Optional[List[ChannelOptionChannelTypes]] = None):
        super().__init__(name=name, description=description, required=required)
        self.type = 7
        self.channel_types: list[ChannelOptionChannelTypes] = channel_types if channel_types else []
        
    def to_dict(self):
        usual_dict: dict = super().to_dict()
        usual_dict["channel_types"] = self.channel_types
        return usual_dict

class RoleOption(BaseSlashCommandOption):
    """
    The RoleOption class.
    Used for options that are roles.

    Attributes
    ----------
    name: :class:`str`
        The name of the option.
    description: :class:`str`
        The description of the option.
    required: :class:`bool`
        Whether the option is required or not.

    Parameters
    ----------
    name: :class:`str`
        The name of the option.
    description: :class:`str`
        The description of the option.
    required: :class:`bool`
        Whether the option is required or not.
    """
    def __init__(self, *, name: str, description: Optional[str] = None, required: bool = True):
        super().__init__(name=name, description=description, required=required)
        self.type = 8


class MentionableOption(BaseSlashCommandOption):
    """
    The MentionableOption class.
    Used for options that are mentionable. It is very broad. Anything that can be mentioned can be used.

    Attributes
    ----------
    name: :class:`str`
        The name of the option.
    description: :class:`str`
        The description of the option.
    required: :class:`bool`
        Whether the option is required or not.

    Parameters
    ----------
    name: :class:`str`
        The name of the option.
    description: :class:`str`
        The description of the option.
    required: :class:`bool`
        Whether the option is required or not.
    """

    def __init__(self, *, name: str, description: Optional[str] = None, required: bool = True):
        super().__init__(name=name, description=description, required=required)
        self.type = 9


class NumberOption(BaseSlashCommandOption):
    """
    The NumberOption class.
    Used for options that are numbers (Can be an Integer, but could be a float).

    Attributes
    ----------
    name: :class:`str`
        The name of the option.
    description: :class:`str`
        The description of the option.
    required: :class:`bool`
        Whether the option is required or not.
    min_value: :class:`int`
        The minimum value of the option.
    max_value: :class:`int`
        The maximum value of the option.
    autocomplete: :class:`bool`
        Whether the option can be autocompleted or not.


    Parameters
    ----------
    name: :class:`str`
        The name of the option.
    description: :class:`str`
        The description of the option.
    required: :class:`bool`
        Whether the option is required or not.
    min_value: :class:`int`
        The minimum value of the option.
    max_value: :class:`int`
        The maximum value of the option.
    autocomplete: :class:`bool`
        Whether the option can be autocompleted or not.

    """
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
    """
    The AttachmentOption class.
    Used for options that are attachments.

    Attributes
    ----------
    name: :class:`str`
        The name of the option.
    description: :class:`str`
        The description of the option.
    required: :class:`bool`
        Whether the option is required or not.


    Parameters
    ----------
    name: :class:`str`
        The name of the option.
    description: :class:`str`
        The description of the option.
    required: :class:`bool`
        Whether the option is required or not.
    """

    def __init__(self, *, name: str, description: Optional[str] = None, required: bool = True):
        super().__init__(name=name, description=description, required=required)
        self.type = 11


class SlashCommandOptionChoice:
    """
    The SlashCommandOptionChoice class.
    Used for options that you would like to have static choices which are the only available values.

    Attributes
    ----------
    name: :class:`str`
        The name of the choice.
    value: :class:`str`
        The value of the choice which will be returned to you.

    """
    def __init__(self, * name: str, value: Union[float, int, str]):
        self.name: str = name
        self.value: Union[float, int, str] = value
    
    def to_dict(self):
        """
        A dictionary representation of the Choice.
        """
        return {
            "name": self.name,
            "value": self.value
        }

class Subcommand(BaseSlashCommandOption):
    """
    The Subcommand class.
    Used for options that are subcommands.

    Attributes
    ----------
    name: :class:`str`
        The name of the subcommand
    description: :class:`str`
        The description of the subcommand
    options: :class:`list`
        The options of the subcommand.
    
    Parameters
    ----------
    name: :class:`str`
        The name of the subcommand
    description: :class:`str`
        The description of the subcommand
    options: :class:`list`
        The options of the subcommand.
    
    """
    def __init__(self, *, name: str, description: str = None, options: list[Union[StringOption, IntegerOption, BooleanOption, UserOption, ChannelOption, RoleOption, MentionableOption, NumberOption]] = []):
        super().__init__(name = name, description = description)
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

        self.options: Union[Subcommand, SubcommandGroup, StringOption, IntegerOption, BooleanOption, UserOption, ChannelOption, RoleOption, MentionableOption, NumberOption] = converted_options

class SubcommandGroup(BaseSlashCommandOption):
    """
    The SubcommandGroup class.
    Used to group subcommands.

    Attributes
    ----------
    name: :class:`str`
        The name of the subcommand group
    description: :class:`str`
        The description of the subcommand group
    options: :class:`list`
        The subcommands.

    Attributes
    ----------
    name: :class:`str`
        The name of the subcommand group
    description: :class:`str`
        The description of the subcommand group
    options: :class:`list`
        The subcommands.
    """

    def __init__(self, *, name: str, description: str = None, options: List[Subcommand] = None):
        super().__init__(name=name, description=description)
        self.type = 2
        self.options = [Subcommand(**option) for option in options]            

    def to_dict(self):
        usual_dict = super().to_dict()        
        usual_dict["options"] = self.options
        return usual_dict


AnyOption = Union[Subcommand, SubcommandGroup, StringOption, IntegerOption, BooleanOption, UserOption, ChannelOption, RoleOption, MentionableOption, NumberOption]

class ClientUserCommand:
    """
    A class to represent a User Command that the Client owns.

    Attributes:
    -----------
    name: :class:`str`
        The name of the command.
    callback: :class:`callable`
        The callback function.

    Parameters:
    -----------
    name: :class:`str`
        The name of the command.
    callback: :class:`callable`
        The callback function.    
    """
    def __init__(self, *, name: str, callback: callable):
        self.name: str = name
        self.callback: callable = callback
    
    @property
    def type(self):
        return 2

class ClientSlashCommand:
    """
    A class to represent a Slash Command that the Client owns.
    
    Attributes
    ----------
    name: :class:`str`
        The name of the command.
    callback: :class:`callable`
        The callback function.
    description: :class:`str`
        The description of the command.
    options: :class:`list`
        The options of the command.

    Parameters
    ----------
    name: :class:`str`
        The name of the command.
    callback: :class:`callable`
        The callback function.
    description: :class:`str`
        The description of the command.
    options: :class:`list`
        The options of the command.
    """
    def __init__(self, *, name: str, callback: callable, description: str = None, options: List[AnyOption] = None):
        self.name: str = name
        self.callback: callable = callback
        self.description: str = description
        self.options: List[AnyOption] = options
    
    @property
    def type(self):
        return 1
    

class ClientMessageCommand(ClientUserCommand):
    """
    A class to represent a Message Command that the Client owns.
    """
    @property
    def type(self):
        return 3
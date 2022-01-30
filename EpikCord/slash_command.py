from typing import (
    Optional,
    List,
    Union
)
from .application import ApplicationCommand

class BaseSlashCommandOption:
    def __init__(self, *, name: str, description: str, required: bool = False):
        self.settings = {
            "name": name,
            "description": description,
            "required": required
        }
        # People shouldn't use this class, this is just a base class for other options

class Subcommand(BaseSlashCommandOption):
    def __init__(self, *, name: str, description: Optional[str] = None, required: bool = False):
        super().__init__(name=name, description=description, required=required)
        self.settings["type"] = 1
        
class SubCommandGroup(BaseSlashCommandOption):
    def __init__(self, *, name: str, description: Optional[str] = None, required: bool = False):
        super().__init__(name=name, description=description, required=required)
        self.settings["type"] = 2
        
class StringOption(BaseSlashCommandOption):
    def __init__(self, *, name: str, description: Optional[str] = None, required: bool = False):
        super().__init__(name=name, description=description, required=required)
        self.settings["type"] = 3
        
class IntegerOption(BaseSlashCommandOption):
    def __init__(self, *, name: str, description: Optional[str] = None, required: bool = False):
        super().__init__(name=name, description=description, required=required)
        self.settings["type"] = 4
        
class BooleanOption(BaseSlashCommandOption):
    def __init__(self, *, name: str, description: Optional[str] = None, required: bool = False):
        super().__init__(name=name, description=description, required=required)
        self.settings["type"] = 5
        
class UserOption(BaseSlashCommandOption):
    def __init__(self, *, name: str, description: Optional[str] = None, required: bool = False):
        super().__init__(name=name, description=description, required=required)
        self.settings["type"] = 6
        
class ChannelOption(BaseSlashCommandOption):
    def __init__(self, *, name: str, description: Optional[str] = None, required: bool = False):
        super().__init__(name=name, description=description, required=required)
        self.settings["type"] = 7
        
class RoleOption(BaseSlashCommandOption):
    def __init__(self, *, name: str, description: Optional[str] = None, required: bool = False):
        super().__init__(name=name, description=description, required=required)
        self.settings["type"] = 8

class MentionableOption(BaseSlashCommandOption):
    def __init__(self, *, name: str, description: Optional[str] = None, required: bool = False):
        super().__init__(name=name, description=description, required=required)
        self.settings["type"] = 9
    
class NumberOption(BaseSlashCommandOption):
    def __init__(self, *, name: str, description: Optional[str] = None, required: bool = False):
        super().__init__(name=name, description=description, required=required)
        self.settings["type"] = 10

class SlashCommandOptionChoice:
    def __init__(self, * name: str, value: Union[float, int, str]):
        self.settings = {
            "name": name,
            "value": value
        }

class SlashCommand(ApplicationCommand):
    def __init__(self, data: dict):
        super().__init__(data)
        self.options: Optional[List[Union[Subcommand, SubCommandGroup, StringOption, IntegerOption, BooleanOption, UserOption, ChannelOption, RoleOption, MentionableOption, NumberOption]]] = data["options"] or None # Return the type hinted class later this will take too long and is very tedious, I'll probably get Copilot to do it for me lmao
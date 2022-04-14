from typing import Optional, List
from .options import AnyOption

class ClientUserCommand:
    """
    A class to represent a User Command that the Client owns.

    Attributes:
    -----------
        * name The name set for the User Command
        * callback: callable The function to call for the User Command (Passed in by the library)

    Parameters:
    -----------
    All parameters follow the documentation of the Attributes accordingly
        * name
        * callback
    """
    def __init__(self, *, name: str, callback: callable): # TODO: Check if you can make GuildUserCommands etc
        self.name: str = name
        self.callback: callable = callback
    
    @property
    def type(self):
        return 2

class ClientSlashCommand:
    def __init__(self, *, name: str, description: str, callback: callable, guild_ids: Optional[List[str]], options: Optional[List[AnyOption]]):
        self.name: str = name
        self.description: str = description
        self.callback: callable = callback
        self.guild_ids: Optional[List[str]] = guild_ids
        self.options: Optional[List[AnyOption]] = options
        self.autocomplete_options: dict = {}

    @property
    def type(self):
        return 1

    def option_autocomplete(self, option_name: str):
        def wrapper(func):
            self.autocomplete_options[option_name] = func
        return wrapper

class ClientMessageCommand(ClientUserCommand):

    @property
    def type(self):
        return 3

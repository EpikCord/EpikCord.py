from typing import List, Union, Callable, Optional
from .exceptions import *
from aiohttp import *
from .__main__ import __version__
class Client(WebsocketClient):

    def __init__(self, token: str, intents: int = 0):
        super().__init__(token, intents)

        self.commands: List[Union[ClientSlashCommand, ClientUserCommand, ClientMessageCommand]] = [] # TODO: Need to change this to a Class Later
        self.guilds: GuildManager = GuildManager(self)
        self._checks: List[Callable] = []

        self.http = HTTPClient(
            # raise_for_status = True,
            headers = {
                "Authorization": f"Bot {token}",
                "User-Agent": f"DiscordBot (https://github.com/EpikCord/EpikCord.py {__version__()})"
            }
        )

        self.utils = Utils(self.http)

        self.user: ClientUser = None
        self.application: Application = None
        self.sections: List[Section] = []

    def command(self, *, name: Optional[str] = None, description: Optional[str] = None, guild_ids: Optional[List[str]] = [], options: Optional[AnyOption] = []):
        def register_slash_command(func):
            if not description and not func.__doc__:
                raise TypeError(f"Missing description for command {func.__name__}.")
            desc = description or func.__doc__
            self.commands.append(ClientSlashCommand(**{
                "callback": func,
                "name": name or func.__name__,
                "description": desc,
                "guild_ids": guild_ids,
                "options": options,
            })) # Cheat method.
        return register_slash_command

    def user_command(self, name: Optional[str] = None):
        def register_slash_command(func):
            self.commands.append(ClientUserCommand(**{
                "callback": func,
                "name": name or func.__name__,
            }))
        return register_slash_command

    def message_command(self, name: Optional[str] = None):
        def register_slash_command(func):
            self.commands.append(ClientMessageCommand(**{
                "callback": func,
                "name": name or func.__name__,
            }))
        return register_slash_command

    def add_section(self, section: Section):
        if not issubclass(section, Section):
            raise InvalidArgumentType("You must pass in a class that inherits from the Section class.")

        for name, command_object in section.commands:
            self.commands[name] = command_object

        for event_name, event_func in section.events:
            self.events[event_name.lower()] = event_func
        self.sections.append(section)
        section.on_load()
    
    def unload_section(self, section: Section):
        if not issubclass(section, Section):
            raise InvalidArgumentType("You must pass in a class that inherits from the Section class.")

        for name, command_object in section.commands:
            del self.commands[name]

        for event_name, event_func in section.events:
            del self.events[event_name.lower()]
        self.sections.remove(section)
        section.on_unload()

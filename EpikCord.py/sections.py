from typing import Optional, List
from .commands import ClientMessageCommand, ClientSlashCommand, ClientUserCommand, AnyOption

class EventsSection:
    """
    A class to represent the Events section of the Client.
    Used to group events into separate files for cleaner code.

    Attributes
    ----------
    client: :class:`Client`
        The client that owns the Events section.
    events: :class:`dict`
        The events in the Events section.

    Parameters
    ----------
    client: :class:`Client`
        The client that owns the Events section.
    events: :class:`dict`
        The events in the Events section.
    """
    def __init__(self, client):
        self.client = client
        self.events = {}

        class _:
            client = ...
            events = ...

        temp = _()
        for event in dir(self):
            if event not in dir(temp):
                self.events[event] = getattr(self, event)

def command(*, name: Optional[str] = None, description: Optional[str] = None, guild_ids: Optional[List[str]] = [], options: Optional[AnyOption] = []):
    """
    A decorator to add a `ClientSlashCommand` to a Section.

    Parameters
    ----------
    name: :class:`str`
        The name of the command.
    description: :class:`str`
        The description of the command.
    guild_ids: :class:`list`
        The guilds that the command is available in.
    options: :class:`list`
        The options of the command.
    """

    def register_slash_command(func):
        if not description and not func.__doc__:
            raise TypeError(f"Missing description for command {func.__name__}.")
        desc = description or func.__doc__
        func.__self__.commands.append(ClientSlashCommand(**{
            "callback": func,
            "name": name or func.__name__,
            "description": desc,
            "guild_ids": guild_ids,
            "options": options,
        })) # Cheat method.
    return register_slash_command

def user_command(name: Optional[str] = None):
    """
    A decorator to add a `ClientUserCommand` to a Section.
    """
    def register_slash_command(func):
        func.__self__.commands.append(ClientUserCommand(**{
            "callback": func,
            "name": name or func.__name__,
        }))
    return register_slash_command

def message_command(name: Optional[str] = None):
    """
    A decorator to add a `ClientMessageCommand` to a Section.
    """
    def register_slash_command(func):
        func.__self__.commands.append(ClientMessageCommand(**{
            "callback": func,
            "name": name or func.__name__,
        }))
    return register_slash_command

class CommandsSection:
    def __init__(self, client):
        self.client = client
        self.commands = {}
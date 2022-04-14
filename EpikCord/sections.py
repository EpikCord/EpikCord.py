from typing import Optional, List

class EventsSection:
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
    def register_slash_command(func):
        func.__self__.commands.append(ClientUserCommand(**{
            "callback": func,
            "name": name or func.__name__,
        }))
    return register_slash_command

def message_command(name: Optional[str] = None):
    def register_slash_command(func):
        func.__self__.commands.append(ClientMessageCommand(**{
            "callback": func,
            "name": name or func.__name__,
        }))
    return register_slash_command

class CommandsSection:
    ...

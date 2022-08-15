from collections import defaultdict
from typing import Union, DefaultDict, List

from .event_handler import Event
from ..commands import ClientMessageCommand, ClientSlashCommand, ClientUserCommand


class Section:
    _cmd = Union[ClientUserCommand, ClientSlashCommand, ClientMessageCommand]

    _commands: DefaultDict[str, List[_cmd]] = defaultdict(list)
    _events: DefaultDict[str, List[Event]] = defaultdict(list)

    def __init_subclass__(cls, **kwargs):
        for attr_value in cls.__dict__.values():
            if isinstance(attr_value, Event):
                cls._events[cls.__name__].append(attr_value)

            elif isinstance(
                attr_value,
                (ClientSlashCommand, ClientUserCommand, ClientMessageCommand),
            ):
                cls._commands[attr_value.name] = attr_value

        super().__init_subclass__(**kwargs)

__all__ = ("Section",)
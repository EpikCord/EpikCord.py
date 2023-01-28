from ..presence import UpdatePresenceData


from enum import IntEnum
from typing import Any, Callable, Coroutine, TypedDict
from typing_extensions import NotRequired, Literal

from discord_typings import IdentifyConnectionProperties

AsyncFunction = Callable[..., Coroutine[Any, Any, Any]]

class OpCode(IntEnum):
    DISPATCH = 0
    HEARTBEAT = 1
    IDENTIFY = 2
    STATUS_UPDATE = 3
    VOICE_STATE_UPDATE = 4
    VOICE_SERVER_PING = 5
    RESUME = 6
    RECONNECT = 7
    REQUEST_GUILD_MEMBERS = 8
    INVALID_SESSION = 9
    HELLO = 10
    HEARTBEAT_ACK = 11


class IdentifyData(TypedDict):
    token: str
    intents: int
    properties: IdentifyConnectionProperties
    compress: bool
    large_threshold: int
    presence: NotRequired[UpdatePresenceData]


class IdentifyCommand(TypedDict):
    op: Literal[OpCode.IDENTIFY]
    d: IdentifyData

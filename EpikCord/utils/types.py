from ..presence import UpdatePresenceData


from enum import IntEnum
from typing import Any, Callable, Coroutine, TypedDict
from typing_extensions import NotRequired, Literal

from discord_typings import IdentifyConnectionProperties

AsyncFunction = Callable[..., Coroutine[Any, Any, Any]]

class OpCode(IntEnum):
    """The opcodes used in the Discord Gateway."""
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
    """The data used in the identify payload."""
    token: str
    intents: int
    properties: IdentifyConnectionProperties
    compress: bool
    large_threshold: int
    presence: NotRequired[UpdatePresenceData]


class IdentifyCommand(TypedDict):
    """The data used to identify with the gateway."""
    op: Literal[OpCode.IDENTIFY]
    d: IdentifyData

class SendingAttachmentData(TypedDict):
    """The data used to send an attachment."""
    id: int
    filename: str
    description: NotRequired[str]
    ephemeral: NotRequired[bool]

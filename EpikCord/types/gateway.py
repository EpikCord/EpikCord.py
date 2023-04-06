from enum import IntEnum
from typing import TypedDict

from discord_typings import IdentifyConnectionProperties
from typing_extensions import Literal, NotRequired

from ..presence import UpdatePresenceData


class OpCode(IntEnum):
    """The opcodes used in the Discord Gateway."""

    DISPATCH = 0
    HEARTBEAT = 1
    IDENTIFY = 2
    PRESENCE_UPDATE = 3
    VOICE_STATE_UPDATE = 4
    RESUME = 6
    RECONNECT = 7
    REQUEST_GUILD_MEMBERS = 8
    INVALID_SESSION = 9
    HELLO = 10
    HEARTBEAT_ACK = 11


class GatewayCloseCode(IntEnum):
    """The close codes used in the Discord Gateway."""

    NORMAL_CLOSURE = 1000
    GOING_AWAY = 1001
    ABNORMAL_CLOSURE = 1006
    UNKNOWN_ERROR = 4000
    UNKNOWN_OPCODE = 4001
    DECODE_ERROR = 4002
    NOT_AUTHENTICATED = 4003
    AUTHENTICATION_FAILED = 4004
    ALREADY_AUTHENTICATED = 4005
    INVALID_SEQUENCE = 4007
    RATE_LIMITED = 4008
    SESSION_TIMED_OUT = 4009
    INVALID_SHARD = 4010
    SHARDING_REQUIRED = 4011
    INVALID_API_VERSION = 4012
    INVALID_INTENTS = 4013
    DISALLOWED_INTENTS = 4014


class VoiceOpCode(IntEnum):
    """The opcodes used in the Discord Voice WebSocket connection."""

    IDENTIFY = 0
    SELECT_PROTOCOL = 1
    READY = 2
    HEARTBEAT = 3
    SESSION_DESCRIPTION = 4
    SPEAKING = 5
    HEARTBEAT_ACK = 6
    RESUME = 7
    HELLO = 8
    RESUMED = 9
    CLIENT_DISCONNECT = 13


class VoiceCloseCode(IntEnum):
    """The close codes used in the Discord Voice WebSocket connection."""

    UNKNOWN_OPCODE = 4001
    FAILED_TO_DECODE_PAYLOAD = 4002
    NOT_AUTHENTICATED = 4003
    AUTHENTICATION_FAILED = 4004
    ALREADY_AUTHENTICATED = 4005
    SESSION_NO_LONGER_VALID = 4006
    SESSION_TIMEOUT = 4009
    SERVER_NOT_FOUND = 4011
    UNKNOWN_PROTOCOL = 4012
    DISCONNECTED = 4014
    VOICE_SERVER_CRASHED = 4015
    UNKNOWN_ENCRYPTION_MODE = 4016


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

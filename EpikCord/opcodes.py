from enum import IntEnum


class Opcode(IntEnum):
    ...


class GatewayOpcode(Opcode):
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


class VoiceOpcode(Opcode):
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


__all__ = ("GatewayOpcode", "VoiceOpcode")

from enum import IntEnum


class GatewayCECode(IntEnum):
    """Gateway close event code."""
    WEBSOCKET_ERROR = 1006

    UnknownError = 4000

    UnknownOpcode = 4001
    DecodeError = 4002

    NotAuthenticated = 4003

    AuthenticationFailed = 4004
    AlreadyAuthenticated = 4005

    InvalidSequence = 4007
    RateLimited = 4008
    SessionTimedOut = 4009

    InvalidShard = 4010
    ShardingRequired = 4011

    InvalidAPIVersion = 4012
    InvalidIntents = 4013
    DisallowedIntents = 4014


class VoiceCECode(IntEnum):
    """Voice close event code."""

    UnknownOpcode = 4001

    DecodeError = 4002

    NotAuthenticated = 4003

    AuthenticationFailed = 4004

    AlreadyAuthenticated = 4005

    SessionExpired = 4006
    SessionTimedOut = 4009

    ServerNotFound = 4011
    UnknownProtocol = 4012

    Disconnected = 4013
    VoiceServerCrash = 4014
    UnknownEncryptionMode = 4015


__all__ = ("GatewayCECode", "VoiceCECode")

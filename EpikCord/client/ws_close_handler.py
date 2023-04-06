import logging
from functools import partial
from typing import Dict, Optional, Type

from ..exceptions import (
    DisallowedIntents,
    GatewayRateLimited,
    InvalidIntents,
    InvalidToken,
    ShardingRequired,
)
from ..types import GatewayCloseCode

logger = logging.getLogger("EpikCord.websocket")


class CloseHandler:
    def __init__(self, resumable: bool = True):
        self.resumable = resumable


class CloseHandlerRaise(CloseHandler):
    def __init__(
        self, exception: Type[Exception], message: Optional[str] = None
    ):
        super().__init__(resumable=False)
        self.exception = exception
        self.message = message


class CloseHandlerLog(CloseHandler):
    def __init__(
        self, message: str, resumable: bool = True, need_report: bool = False
    ):
        super().__init__(resumable=resumable)
        self.message = message
        self.need_report = need_report


_ignore = CloseHandler()
CloseHandlerLogReported = partial(CloseHandlerLog, need_report=True)

_close_disallowed_intents = CloseHandlerRaise(
    DisallowedIntents,
    "You cannot use privileged intents with this token, go to the developer"
    " portal and allow the privileged intents needed. ",
)
_close_authentication_failed = CloseHandlerRaise(
    InvalidToken, "The token you provided is invalid."
)
_close_rate_limited = CloseHandlerRaise(
    GatewayRateLimited,
    "You've been rate limited. Try again in a few minutes.",
)
_close_sharding_required = CloseHandlerRaise(
    ShardingRequired, "You need to shard the bot."
)
_close_invalid_api_version = CloseHandlerRaise(
    DeprecationWarning,
    "The gateway you're connecting to is deprecated and does not work,"
    " update EpikCord.",
)
_close_invalid_intents = CloseHandlerRaise(
    InvalidIntents, "The intents you provided are invalid."
)
_close_unknown_opcode = CloseHandlerLogReported(
    "EpikCord.py sent an invalid OPCODE to the Gateway."
)
_close_decode_error = CloseHandlerLogReported(
    "EpikCord.py sent an invalid payload to the Gateway."
)
_close_not_authenticated = CloseHandlerLog(
    "EpikCord.py has sent a payload prior to identifying.",
    resumable=False,
    need_report=True,
)
_close_already_authenticated = CloseHandlerLogReported(
    "EpikCord.py tried to authenticate again."
)
_close_invalid_sequence = CloseHandlerLogReported(
    "EpikCord.py sent an invalid sequence number."
)
_close_session_timed_out = CloseHandlerLog("Session timed out.")

close_dispatcher: Dict[GatewayCloseCode, CloseHandler] = {
    GatewayCloseCode.ABNORMAL_CLOSURE: _ignore,
    GatewayCloseCode.UNKNOWN_ERROR: _ignore,
    GatewayCloseCode.DISALLOWED_INTENTS: _close_disallowed_intents,
    GatewayCloseCode.AUTHENTICATION_FAILED: _close_authentication_failed,
    GatewayCloseCode.RATE_LIMITED: _close_rate_limited,
    GatewayCloseCode.SHARDING_REQUIRED: _close_sharding_required,
    GatewayCloseCode.INVALID_API_VERSION: _close_invalid_api_version,
    GatewayCloseCode.INVALID_INTENTS: _close_invalid_intents,
    GatewayCloseCode.UNKNOWN_OPCODE: _close_unknown_opcode,
    GatewayCloseCode.DECODE_ERROR: _close_decode_error,
    GatewayCloseCode.NOT_AUTHENTICATED: _close_not_authenticated,
    GatewayCloseCode.ALREADY_AUTHENTICATED: _close_already_authenticated,
    GatewayCloseCode.INVALID_SEQUENCE: _close_invalid_sequence,
    GatewayCloseCode.SESSION_TIMED_OUT: _close_session_timed_out,
}

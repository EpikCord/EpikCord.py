import logging
from typing import Dict, Optional, Type

from ..exceptions import (
    DisallowedIntents,
    GatewayRateLimited,
    InvalidIntents,
    InvalidToken,
    ShardingRequired,
)
from ..utils import GatewayCloseCode

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


ignore = CloseHandler()
close_dispatcher: Dict[GatewayCloseCode, CloseHandler] = {
    GatewayCloseCode.ABNORMAL_CLOSURE: ignore,
    GatewayCloseCode.UNKNOWN_ERROR: ignore,
    GatewayCloseCode.DISALLOWED_INTENTS: CloseHandlerRaise(
        DisallowedIntents,
        "You cannot use privileged intents with this token, go to "
        "the developer portal and allow the privileged intents "
        "needed. ",
    ),
    GatewayCloseCode.AUTHENTICATION_FAILED: CloseHandlerRaise(
        InvalidToken, "The token you provided is invalid."
    ),
    GatewayCloseCode.RATE_LIMITED: CloseHandlerRaise(
        GatewayRateLimited,
        "You've been rate limited. Try again in a few minutes.",
    ),
    GatewayCloseCode.SHARDING_REQUIRED: CloseHandlerRaise(
        ShardingRequired, "You need to shard the bot."
    ),
    GatewayCloseCode.INVALID_API_VERSION: CloseHandlerRaise(
        DeprecationWarning,
        "The gateway you're connecting to is deprecated and does not "
        "work, update EpikCord.",
    ),
    GatewayCloseCode.INVALID_INTENTS: CloseHandlerRaise(
        InvalidIntents, "The intents you provided are invalid."
    ),
    GatewayCloseCode.UNKNOWN_OPCODE: CloseHandlerLog(
        "EpikCord.py sent an invalid OPCODE to the Gateway. ", need_report=True
    ),
    GatewayCloseCode.DECODE_ERROR: CloseHandlerLog(
        "EpikCord.py sent an invalid payload to the Gateway.", need_report=True
    ),
    GatewayCloseCode.NOT_AUTHENTICATED: CloseHandlerLog(
        "EpikCord.py has sent a payload prior to identifying.",
        resumable=False,
        need_report=True,
    ),
    GatewayCloseCode.ALREADY_AUTHENTICATED: CloseHandlerLog(
        "EpikCord.py tried to authenticate again.", need_report=True
    ),
    GatewayCloseCode.INVALID_SEQUENCE: CloseHandlerLog(
        "EpikCord.py sent an invalid sequence number.", need_report=True
    ),
    GatewayCloseCode.SESSION_TIMED_OUT: CloseHandlerLog("Session timed out."),
}

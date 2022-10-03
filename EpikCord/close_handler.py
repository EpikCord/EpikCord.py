import logging
from typing import Dict, Optional, Type

from .close_event_codes import GatewayCECode
from .exceptions import (
    DisallowedIntents,
    InvalidIntents,
    InvalidToken,
    Ratelimited429,
    ShardingRequired,
)

logger = logging.getLogger(__name__)


class CloseHandler:
    def __init__(self, resumable: bool = True):
        self.resumable = resumable


class CloseHandlerRaise(CloseHandler):
    def __init__(self, exception: Type[Exception], message: Optional[str] = None):
        super().__init__(resumable=False)
        self.exception = exception
        self.message = message


class CloseHandlerLog(CloseHandler):
    def __init__(self, message: str, resumable: bool = True, need_report: bool = False):
        super().__init__(resumable=resumable)
        self.message = message
        self.need_report = need_report


ignore = CloseHandler()
close_dispatcher: Dict[GatewayCECode, CloseHandler] = {
    GatewayCECode.AbnormalClosure: ignore,
    GatewayCECode.UnknownError: ignore,
    GatewayCECode.DisallowedIntents: CloseHandlerRaise(
        DisallowedIntents,
        "You cannot use privileged intents with this token, go to "
        "the developer portal and allow the privileged intents "
        "needed. ",
    ),
    GatewayCECode.AuthenticationFailed: CloseHandlerRaise(
        InvalidToken, "The token you provided is invalid."
    ),
    GatewayCECode.RateLimited: CloseHandlerRaise(
        Ratelimited429, "You've been rate limited. Try again in a few minutes."
    ),
    GatewayCECode.ShardingRequired: CloseHandlerRaise(
        ShardingRequired, "You need to shard the bot."
    ),
    GatewayCECode.InvalidAPIVersion: CloseHandlerRaise(
        DeprecationWarning,
        "The gateway you're connecting to is deprecated and does not "
        "work, upgrade EpikCord.py. ",
    ),
    GatewayCECode.InvalidIntents: CloseHandlerRaise(
        InvalidIntents, "The intents you provided are invalid."
    ),
    GatewayCECode.UnknownOpcode: CloseHandlerLog(
        "EpikCord.py sent an invalid OPCODE to the Gateway. ", need_report=True
    ),
    GatewayCECode.DecodeError: CloseHandlerLog(
        "EpikCord.py sent an invalid payload to the Gateway.", need_report=True
    ),
    GatewayCECode.NotAuthenticated: CloseHandlerLog(
        "EpikCord.py has sent a payload prior to identifying.",
        resumable=False,
        need_report=True,
    ),
    GatewayCECode.AlreadyAuthenticated: CloseHandlerLog(
        "EpikCord.py tried to authenticate again.", need_report=True
    ),
    GatewayCECode.InvalidSequence: CloseHandlerLog(
        "EpikCord.py sent an invalid sequence number.", need_report=True
    ),
    GatewayCECode.SessionTimedOut: CloseHandlerLog("Session timed out."),
}

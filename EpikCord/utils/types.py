from typing import Any, Callable, Coroutine, TypedDict

from discord_typings import IdentifyConnectionProperties
from typing_extensions import Literal, NotRequired

from ..presence import UpdatePresenceData

AsyncFunction = Callable[..., Coroutine[Any, Any, Any]]


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

    op: Literal[2]
    d: IdentifyData


class SendingAttachmentData(TypedDict):
    """The data used to send an attachment."""

    id: int
    filename: str
    description: NotRequired[str]
    ephemeral: NotRequired[bool]

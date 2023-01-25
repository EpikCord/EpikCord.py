from enum import Enum, IntEnum
from typing import Optional, TypedDict, List
from typing_extensions import NotRequired

class ActivityPayload(TypedDict): # Data sent to Discord when updating presence
    name: str
    type: int
    url: NotRequired[str]


class Status(Enum):
    ONLINE = "online"
    IDLE = "idle"
    DND = "dnd"
    INVISIBLE = "invisible"
    OFFLINE = "offline"


class ActivityType(IntEnum):
    GAME = 0
    STREAMING = 1
    LISTENING = 2
    WATCHING = 3
    CUSTOM = 4
    COMPETING = 5

class UpdatePresenceData(TypedDict): # Data sent to Discord when updating presence
    status: NotRequired[str]
    activities: NotRequired[List[ActivityPayload]]
    afk: NotRequired[bool]
    since: NotRequired[float]

class Activity:
    def __init__(self, *, name: str, type: ActivityType, url: Optional[str] = None):
        """Represents a Discord activity.

        Parameters
        ----------
        name: :class:`str`
            The name of the activity.
        type: :class:`ActivityType`
            The type of the activity.
        url: Optional[:class:`str`]
            The url of the activity. Only used for streaming (activity type 1).
        """
        self.name = name
        self.type = type
        self.url = url

    def to_dict(self) -> ActivityPayload:
        """Converts the activity to a dictionary."""
        data: ActivityPayload = {"name": self.name, "type": self.type.value}

        if self.url is not None and not self.type == ActivityType.STREAMING:
            raise ValueError("URL can only be set for streaming activities.")

        if self.url is not None:
            data["url"] = self.url

        return data


class Presence:
    def __init__(self, *, status: Optional[Status] = None, activity: Optional[Activity] = None, afk: bool = False, since: float = 0):
        """Represents a Discord presence.

        Parameters
        ----------
        status: Optional[:class:`Status`]
            The status of the presence.
        activity: Optional[:class:`Activity`]
            The activity of the presence.
        afk: :class:`bool`
            Whether the the bot is afk or not. Defaults to False.
        since: Optional[:class:`float`]
            The time since the bot has been afk. Defaults to 0.
        """
        if not status and not activity:
            raise ValueError("Presence must have either a status or an activity.")
        self.status: Optional[Status] = status
        self.activity: Optional[Activity] = activity
        self.afk: bool = afk
        self.since: float = since

    def to_dict(self) -> UpdatePresenceData:
        """Converts the presence to a dictionary."""
        data: UpdatePresenceData = {}

        if self.status is not None:
            data["status"] = self.status.value

        if self.activity is not None:
            data["activities"] = [self.activity.to_dict()]

        if self.afk:
            data["afk"] = self.afk

        if self.since:
            data["since"] = self.since

        return data
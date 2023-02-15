from enum import Enum, IntEnum
from typing import List, Optional, TypedDict

from typing_extensions import NotRequired


class ActivityPayload(TypedDict):  # Data sent to Discord when updating presence
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


class UpdatePresenceData(TypedDict):
    # Data sent to Discord when updating presence
    status: NotRequired[str]
    activities: NotRequired[List[ActivityPayload]]
    afk: bool
    since: float


class Activity:
    def __init__(
        self, *, name: str, ac_type: ActivityType, url: Optional[str] = None
    ):
        """Represents a Discord activity.

        Parameters
        ----------
        name: :class:`str`
            The name of the activity.
        ac_type: :class:`ActivityType`
            The type of the activity.
        url: Optional[:class:`str`]
            The url of the activity. Only used for streaming (activity type 1).
        """
        self.name = name
        self.type = ac_type
        self.url = url

    def to_dict(self) -> ActivityPayload:
        """Converts the activity to a dictionary."""
        data: ActivityPayload = {"name": self.name, "type": self.type.value}

        if self.url is None:
            return data

        if self.type != ActivityType.STREAMING:
            raise ValueError("URL can only be set for streaming activities.")

        data["url"] = self.url
        return data


class Presence:
    def __init__(
        self,
        *,
        status: Optional[Status] = None,
        activity: Optional[Activity] = None,
    ):
        """Represents a Discord presence.

        Parameters
        ----------
        status: Optional[:class:`Status`]
            The status of the presence.
        activity: Optional[:class:`Activity`]
            The activity of the presence.
        """
        if not status and not activity:
            raise ValueError(
                "Presence must have either a status or an activity."
            )
        self.status: Optional[Status] = status
        self.activity: Optional[Activity] = activity

    def to_dict(self) -> UpdatePresenceData:
        """Converts the presence to a dictionary."""
        data: UpdatePresenceData = {
            "afk": False,
            "since": 0.0,
        }

        if self.status is not None:
            data["status"] = self.status.value

        if self.activity is not None:
            data["activities"] = [self.activity.to_dict()]

        return data


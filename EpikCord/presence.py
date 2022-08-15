from typing import Optional, List
from .exceptions import InvalidStatus, InvalidData


class Status:
    """The class which represents a Status.

    Attributes
    ----------
    status : str
        The status of the user.
    """

    def __init__(self, status: str):
        """Represents a Status.

        Arguments
        ---------
        status : str
            The status of the user.
            Either ``online``, ``idle``, ``dnd`` or ``invisible``.

        Raises
        ------
        InvalidStatus
            The status that you supplied is not valid.
        """
        if status not in {"online", "dnd", "idle", "invisible", "offline"}:
            raise InvalidStatus("That is an invalid status.")

        self.status = status if status != "offline" else "invisible"


class Activity:
    """Represents a Discord Activity object.

    Attributes
    ---------
    name : str
        The name of the activity.
    type : int
        The type of the activity.
    url : Optional[str]
        The url of the activity.
        Only available for the streaming activity

    """

    def __init__(self, *, name: str, type: int, url: Optional[str] = None):
        """Represents a Discord Activity object.

        Arguments
        ---------
        name : str
            The name of the activity.
        type : int
            The type of the activity.
        url : Optional[str]
            The url of the activity.
            Only available for the streaming activity.
        """
        self.name = name
        self.type = type
        self.url = url

    def to_dict(self):
        """Returns activity class as dict

        Returns
        -------
        payload : dict
            The dict representation of the Activity.

        Raises
        ------
            InvalidData
                You tried to set an url for a non-streaming activity.
        """
        payload = {
            "name": self.name,
            "type": self.type,
        }

        if self.url:
            if self.type != 1:
                raise InvalidData("You cannot set a URL")
            payload["url"] = self.url

        return payload


class Presence:
    """
    A class representation of a Presence.

    Attributes
    ----------
    activity : Optional[Activity]
        The activity of the user.
    status : Status
        The status of the user.
    """

    def __init__(
        self,
        *,
        activity: Optional[Activity] = None,
        status: Optional[Status] = None,
    ):
        """
        Arguments
        ---------
        activity : Optional[Activity]
            The activity of the user.
        status : Status
            The status of the user.
        """
        self.activity: Optional[Activity] = activity
        self.status: Status = status.status if isinstance(status, Status) else status

    def to_dict(self):
        """
        The dict representation of the Presence.

        Returns
        -------
        payload : dict
            The dict representation of the Presence.
        """
        payload = {}

        if self.status:
            payload["status"] = self.status

        if self.activity:
            payload["activity"] = [self.activity.to_dict()]

        return payload


__all__ = ("Status", "Activity", "Presence")

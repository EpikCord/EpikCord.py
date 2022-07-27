from typing import (
    List,
    Callable, Optional
)

class BaseCommand:
    def __init__(self):
        self.checks: List[Check] = []

    def is_slash_command(self):
        return self.type == 1

    def is_user_command(self):
        return self.type == 2

    def is_message_command(self):
        return self.type == 3

    @property
    def type(self):
        ...


class ClientUserCommand(BaseCommand):
    """
    A class to represent a User Command that the Client owns.

    Attributes:
    -----------
        * name The name set for the User Command
        * callback: callable The function to call for the User Command
        (Passed in by the library)

    Parameters:
    -----------
    All parameters follow the documentation of the Attributes accordingly
        * name
        * callback
    """

    def __init__(self, *, name: str, callback: Callable):
        super().__init__()
        self.name: str = name
        self.callback: Callable = callback

    @property
    def type(self):
        return 2


class ClientSlashCommand(BaseCommand):
    def __init__(
        self,
        *,
        name: str,
        description: str,
        callback: Callable,
        guild_ids: Optional[List[str]] = None,
        options: Optional[List[AnyOption]] = None,
        name_localization: Optional[Localization] = None,
        description_localization: Optional[str] = None,
    ):
        super().__init__()
        self.name: str = name
        self.description: str = description
        self.name_localizations: Optional[Localization] = name_localization
        self.description_localizations: Optional[
            Localization
        ] = description_localization
        self.callback: Callable = callback
        self.guild_ids: Optional[List[str]] = guild_ids or []
        self.options: Optional[List[AnyOption]] = options or []
        self.autocomplete_options: dict = {}

    @property
    def type(self):
        return 1

    def option_autocomplete(self, option_name: str):
        def wrapper(func):
            self.autocomplete_options[option_name] = func

        return wrapper

    def to_dict(self):
        payload = {
            "name": self.name,
            "description": self.description,
            "type": self.type,
            "options": [option.to_dict() for option in self.options],
        }

        if self.name_localizations:
            payload["name_localizations"] = [
                l.to_dict() for l in self.name_localizations
            ]
        if self.description_localizations:
            payload["description_localizations"] = [
                l.to_dict() for l in self.description_localizations
            ]
        return payload


class ClientMessageCommand(ClientUserCommand):
    @property
    def type(self):
        return 3

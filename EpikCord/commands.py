from logging import getLogger
from typing import Any, Callable, Coroutine, List, Optional

from .abstract import BaseCommand
from .exceptions import FailedCheck
from .localizations import Localization
from .options import AnyOption

logger = getLogger(__name__)


Callback = Callable[..., Coroutine[Any, Any, Any]]


class Check:
    def __init__(self, callback: Callback):
        self.callback: Callback = callback
        self.success_callback: Callback = self._default_success
        self.failure_callback: Callback = self._default_failure

    def success(self, callback: Optional[Callable] = None):
        self.success_callback = callback or self._default_success

    def failure(self, callback: Optional[Callable] = None):
        self.failure_callback = callback or self._default_failure

    async def default_success(self, interaction):
        logger.info(
            f"{interaction.author.username} ({interaction.author.id}) passed "
            f"the check {self.command_callback.__name__}. "
        )

    async def default_failure(self, interaction):
        logger.critical(
            f"{interaction.author.username} ({interaction.author.id}) failed "
            f"the check {self.command_callback.__name__}. "
        )
        raise FailedCheck(
            f"{interaction.author.username} ({interaction.author.id}) failed "
            f"the check {self.command_callback.__name__}. "
        )


class ClientUserCommand(BaseCommand):
    """
    A class to represent a User Command that the Client owns.

    Attributes:
    -----------
        * name: str
            The name set for the User Command
        * callback: Callable
            The function to call for the User Command
            (Passed in by the library)

    Parameters:
    -----------
    All parameters follow the documentation of the Attributes accordingly
        * name
        * callback
        * checks
    """

    def __init__(self, *, name: str, callback: Callable, checks: Optional[List[Check]]):
        super().__init__(checks or [])
        self.name: str = name
        self.callback: Callable = callback

    @property
    def type(self):
        return 2

    def to_dict(self):
        return {"name": self.name}


class ClientSlashCommand(BaseCommand):
    def __init__(
        self,
        *,
        name: str,
        description: str,
        callback: Callable,
        guild_ids: Optional[List[str]] = None,
        options: Optional[List[AnyOption]] = None,
        name_localization: Optional[List[Localization]] = None,
        description_localization: Optional[List[Localization]] = None,
        checks: Optional[List[Check]] = None,
    ):
        super().__init__(checks or [])
        self.name: str = name
        self.description: str = description
        self.name_localizations: Optional[List[Localization]] = name_localization
        self.description_localizations: Optional[
            List[Localization]
        ] = description_localization
        self.callback: Callable = callback
        self.guild_ids: Optional[List[str]] = guild_ids or []
        self.options: Optional[List[AnyOption]] = options or []
        self.autocomplete_options: Dict[str, Callback] = {}

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
                loc.to_dict() for loc in self.name_localizations
            ]
        if self.description_localizations:
            payload["description_localizations"] = [
                loc.to_dict() for loc in self.description_localizations
            ]
        return payload


class ClientMessageCommand(ClientUserCommand):
    @property
    def type(self):
        return 3


__all__ = ("ClientUserCommand", "ClientSlashCommand", "ClientMessageCommand", "Check")

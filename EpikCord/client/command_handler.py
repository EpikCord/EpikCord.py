from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List, Optional, Union

from ..localizations import *
from ..options import AnyOption

if TYPE_CHECKING:
    from .. import Check


class CommandHandler:
    def __init__(self):
        from EpikCord import ClientMessageCommand, ClientSlashCommand, ClientUserCommand

        self.commands: Dict[
            str, Union[ClientSlashCommand, ClientUserCommand, ClientMessageCommand]
        ] = {}
        super().__init__()

    def command(
        self,
        *,
        name: Optional[str] = None,
        description: str = None,
        guild_ids: Optional[List[str]] = None,
        options: Optional[List[AnyOption]] = None,
        name_localizations: Optional[List[Localization]] = None,
        description_localizations: Optional[List[Localization]] = None,
        name_localisations: Optional[List[Localization]] = None,
        description_localisations: Optional[List[Localization]] = None,
        checks: Optional[List[Check]] = None,
    ):
        name_localization = name_localizations, name_localisations or []
        description_localization = (
            description_localizations,
            description_localisations or [],
        )

        def register_slash_command(func):
            desc = description or func.__doc__
            if not desc:
                raise TypeError(
                    f"Command with {name or func.__name__} has no description. This is required."
                )
            from EpikCord import ClientSlashCommand

            command = ClientSlashCommand(
                name=name or func.__name__,
                description=desc,
                guild_ids=guild_ids or [],
                options=options or [],
                callback=func,
                name_localization=name_localization,
                description_localization=description_localization,
                checks=checks or [],
            )

            self.commands[command.name] = command
            return command

        return register_slash_command

    def user_command(
        self, name: Optional[str] = None, checks: Optional[List[Check]] = None
    ):
        def register_slash_command(func):
            from EpikCord import ClientUserCommand

            results = ClientUserCommand(
                callback=func, name=name or func.__name__, checks=checks or []
            )

            self.commands[name] = results
            return results

        return register_slash_command

    def message_command(
        self, name: Optional[str] = None, checks: Optional[List[Check]] = None
    ):
        def register_slash_command(func):
            from EpikCord import ClientMessageCommand

            results = ClientMessageCommand(
                callback=func, name=name or func.__name__, checks=checks or []
            )

            self.commands[name] = results
            return results

        return register_slash_command

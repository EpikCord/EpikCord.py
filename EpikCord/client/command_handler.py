from __future__ import annotations

from inspect import iscoroutinefunction
from logging import getLogger
from typing import TYPE_CHECKING, Dict, List, Optional, Union

from ..application import ApplicationCommand
from ..localizations import *
from ..options import AnyOption, ReceivedOption

if TYPE_CHECKING:
    from .. import Check

logger = getLogger(__name__)


class CommandHandler:
    def __init__(self):
        from EpikCord import ClientMessageCommand, ClientSlashCommand, ClientUserCommand

        self.commands: Dict[
            str, Union[ClientSlashCommand, ClientUserCommand, ClientMessageCommand]
        ] = {}

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

    async def handle_interaction(self, interaction):
        """The function which is the handler for interactions.
        Change this if you want to, to change how your "command handler" works

        Parameters
        ----------
        interaction: Union[ApplicationCommandInteraction, MessageComponentInteraction, AutoCompleteInteraction, ModalSubmitInteraction]
            A subclass of BaseInteraction which represents the Interaction
        """

        if interaction.is_ping:
            return await self.http.post(
                f"interactions/{interaction.id}/{interaction.token}/callback",
                json={"type": 1},
            )

        elif interaction.is_application_command:
            command = self.commands.get(interaction.command_name)

            if not command:
                logger.warning(
                    f"Command {interaction.command_name} is not registered in "
                    f"this code, but is registered with Discord. "
                )
                return  # TODO Possibly add an error which people can handle?

            options = []

            if command.is_user_command() or command.is_message_command():
                options.append(interaction.target_id)

            if command.is_slash_command():
                for check in command.checks:
                    if iscoroutinefunction(check.callback):
                        if not await check.callback(interaction):
                            return await check.failure_callback(interaction)

                    elif not check.callback(interaction):
                        await check.failure_callback(interaction)
                    await check.success_callback(interaction)

                options.extend(ReceivedOption(option) for option in interaction.options)

            try:
                return await command.callback(
                    interaction, *[option.value for option in options]
                )
            except Exception as e:
                await self.command_error(interaction, e)

        if interaction.is_message_component:  # If it's a message component interaction

            if not self._components.get(
                interaction.custom_id
            ):  # If it's registered with the bot
                logger.warning(
                    f"A user tried to interact with a component with the "
                    f"custom id {interaction.custom_id}, but it is not "
                    f"registered in this code, but is on Discord. "
                )

            if interaction.is_button():  # If it's a button
                component = None
                for action_row in interaction.message.components:
                    for component in action_row.components:
                        if component.custom_id == interaction.custom_id:
                            component = component

                return await self._components[interaction.custom_id](
                    interaction, component
                )  # Call the callback

            elif interaction.is_select_menu():

                if not self._components.get(interaction.custom_id):
                    logger.warning(
                        f"A user tried to interact with a component with the "
                        f"custom id {interaction.custom_id}, but it is not "
                        f"registered in this code, but is on Discord. "
                    )
                    return

                component = None
                for action_row in interaction.message.components:
                    for possible_component in action_row.components:
                        if possible_component.custom_id == interaction.custom_id:
                            component = possible_component
                            break

                return await self._components[interaction.custom_id](
                    interaction, component, *interaction.values
                )

        if interaction.is_autocomplete:
            command = self.commands.get(interaction.command_name)
            if not command:
                return
            try:
                option = list(
                    filter(lambda option: option.focused == True, interaction.options)
                )[0]
            except IndexError:
                logger.warning(
                    f"No option was focused for {interaction.command_name} but we still received an autocomplete interaction."
                )
            if auto_complete_callback := command.autocomplete_options.get(option):
                await auto_complete_callback(interaction, ReceivedOption(option))

        if interaction.is_modal_submit:
            action_rows = interaction._components
            component_object_list = []
            for action_row in action_rows:
                component_object_list.extend(
                    component["value"] for component in action_row.get("components")
                )

            await self._components.get(interaction.custom_id)(
                interaction, *component_object_list
            )


__all__ = ("CommandHandler",)

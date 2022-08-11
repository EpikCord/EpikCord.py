from .command_handler import CommandHandler
from ..opcodes import GatewayOpcode
from logging import getLogger
from time import perf_counter_ns
from inspect import iscoroutine
import asyncio
from typing import Optional, Callable
from collections import defaultdict, deque

logger = getLogger(__name__)


class Event:
    def __init__(self, callback: Callable, *, event_name: str):
        self.callback = callback
        self.event_name = event_name or callback.__name__


class EventHandler(CommandHandler):
    # Class that'll contain all methods that'll be called when an event is
    # triggered.

    def __init__(self):
        super().__init__()
        self.events = defaultdict(list)
        self.wait_for_events = defaultdict(list)
        self.latencies = deque(maxlen=5)

    def wait_for(
        self, event_name: str, *, check: Optional[Callable] = None, timeout: int = None
    ):
        """
        Waits for the event to be triggered.

        Parameters
        ----------
        event_name : str
            The name of the event to wait for.
        check : Optional[callable]
            A check to run on the event.
            If it returns ``False``, the event will be ignored.
        timeout : int
            The amount of time to wait for the event.
            If not specified, it'll wait forever.
        """
        timeout = timeout or 0
        future = asyncio.Future()
        if not check:

            def check(*_, **__):
                return True

        self.wait_for_events[event_name.lower()].append((future, check))
        return asyncio.wait_for(future, timeout=timeout)

    @staticmethod
    async def voice_server_update(data: dict):
        voice_data = data["d"]
        payload = {
            "token": voice_data["token"],
            "endpoint": voice_data["endpoint"],
            "guild_id": voice_data["guild_id"],
        }

        if voice_data["endpoint"]:
            payload["endpoint"] = voice_data["endpoint"]

        return payload

    async def voice_state_update(self, data: dict):
        from EpikCord import VoiceState

        return VoiceState(
            self, data
        )  # TODO: Make this return something like (VoiceState, Member) or make VoiceState get Member from member_id

    def component(self, custom_id: str):
        """
        Execute this function when a component with the `custom_id` is interacted with.
        """

        def wrapper(func):
            self._components[custom_id] = func

        return wrapper

    async def guild_members_chunk(self, data: dict):
        ...

    async def guild_delete(self, data: dict):
        return self.guilds.get(data["id"])

    async def handle_events(self):
        async for event in self.ws:
            event = event.json()
            logger.debug(f"Received {event} from Discord.")

            if event["op"] == GatewayOpcode.HELLO:
                self.interval = event["d"]["heartbeat_interval"]

                async def wrapper():
                    while True:
                        await self.heartbeat(False)

                asyncio.create_task(wrapper())
                await self.identify()

            elif event["op"] == GatewayOpcode.DISPATCH:
                await self.handle_event(event)

            elif event["op"] == GatewayOpcode.HEARTBEAT:
                # I shouldn't wait the remaining delay according to the docs.
                await self.heartbeat(True)

            elif event["op"] == GatewayOpcode.HEARTBEAT_ACK:
                heartbeat_ack_time = perf_counter_ns()
                self.discord_latency: int = heartbeat_ack_time - self.heartbeat_time
                self.latencies.append(self.discord_latency)
                try:
                    self.heartbeats.append(event["d"])
                except AttributeError:
                    self.heartbeats = [event["d"]]

            elif event["op"] == GatewayOpcode.RECONNECT:
                await self.reconnect()

            elif event["op"] == GatewayOpcode.RESUMED:
                logger.debug(
                    "Connection successfully resumed and all proceeding events are new."
                )

            if event["op"] != GatewayOpcode.DISPATCH:  # TODO: find op code
                logger.debug(f"Received OPCODE: {event['op']}")

        await self.handle_close()

    async def handle_event(self, event: dict):
        from EpikCord import UnavailableGuild

        self.sequence = event["s"]
        logger.info(f"Received event {event['t']} with data {event['d']}")

        results_from_event = event["d"]

        try:
            results_from_event = (
                await getattr(self, event["t"].lower())(results_from_event)
                if hasattr(self, event["t"].lower())
                else None
            )
            if not results_from_event:
                results_from_event = []
        except Exception as e:
            logger.exception(f"Error handling event {event['t']}: {e}")

        if isinstance(results_from_event, UnavailableGuild):
            return  # This is their lazy backfill which I dislike.

        logger.debug(f"Emitting user event {event['t']}")
        try:
            if results_from_event != event["d"]:

                results_from_event = [results_from_event] if results_from_event else []
                if callbacks := self.events.get(event["t"].lower()):
                    logger.info(
                        f"Calling {len(callbacks)} callbacks for {event['t']} with data {results_from_event}"
                    )
                    for callback in callbacks:
                        await callback(*results_from_event)
            else:
                logger.warning(f"{event['t']} is going to receive unparsed data.")

                if callbacks := self.events.get(event["t"].lower()):
                    for callback in callbacks:
                        await callback(results_from_event)
        except Exception as e:
            logger.exception(f"Error handling user-defined event {event['t']}: {e}")
        if callbacks := self.wait_for_events.get(event["t"].lower()):
            for future, check in callbacks:
                if check(*results_from_event):
                    future.set_result(results_from_event)

    async def handle_interaction(self, interaction):
        """The function which is the handler for interactions.
        Change this if you want to, to change how your "command handler" works

        Arguments
        ---------
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
                    try:
                        if iscoroutine(check.callback(interaction)):
                            await check.callback(interaction)
                        else:
                            check.callback(interaction)
                    except RuntimeError:
                        ...  # Suppress.
                for option in interaction.options:
                    options.append(option.get("value"))
            try:
                return await command.callback(interaction, *options)
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
                    interaction, self.utils.component_from_type(component)
                )  # Call the callback

            elif interaction.is_select_menu():

                def get_select_menu():
                    for action_row in interaction.message.components:
                        for component in action_row["components"]:
                            if component["custom_id"] == interaction.custom_id:
                                component = self.utils.component_from_type(component)
                                return component

                return await self._components[interaction.custom_id](
                    interaction, get_select_menu(), *interaction.values
                )

        if interaction.is_autocomplete:
            command = self.commands.get(interaction.command_name)
            if not command:
                return
            ...  # TODO: Implement autocomplete

        if interaction.is_modal_submit:
            action_rows = interaction._components
            component_object_list = []
            for action_row in action_rows:
                for component in action_row.get("components"):
                    component_object_list.append(
                        component["value"]
                    )  # TODO: Fix this later, component_object_list is empty ;(

            await self._components.get(interaction.custom_id)(
                interaction, *component_object_list
            )

    async def interaction_create(self, data):
        interaction = self.utils.interaction_from_type(data)

        await self.handle_interaction(interaction)

        return interaction

    async def channel_create(self, data: dict):
        channel = self.utils.channel_from_type(data)
        self.channels.add_to_cache(channel.id, channel)
        return channel

    async def message_create(self, data: dict):
        """Event fired when messages are created"""
        from EpikCord import Message

        return Message(self, data)

    async def guild_create(self, data):
        from EpikCord import UnavailableGuild, Guild, Thread

        guild = (
            UnavailableGuild(data)
            if data.get("unavailable") is True
            else Guild(self, data)
            if data.get("unavailable") is False
            else None
        )

        if not guild:
            return

        self.guilds.add_to_cache(guild.id, guild)

        if data.get("unavailable") is None:
            return  # Bot was removed

        for channel in data["channels"]:
            self.channels.add_to_cache(
                data["id"], self.utils.channel_from_type(channel)
            )

        for thread in data["threads"]:
            self.channels.add_to_cache(data["id"], Thread(self, thread))

        return guild

        # TODO: Add other attributes to cache

    def event(self, event_name: Optional[str] = None):
        def register_event(func):
            func_name = event_name or func.__name__.lower()

            if func_name.startswith("on_"):
                func_name = func_name[3:]

            self.events[func_name].append(func)

            return Event(func, event_name=func_name)

        return register_event

    async def guild_member_update(self, data):
        from EpikCord import GuildMember

        guild_member = GuildMember(self, data)
        return self.members.fetch(data["id"]), guild_member

    async def ready(self, data: dict):
        from EpikCord import ClientUser, ClientApplication

        self.user: ClientUser = ClientUser(self, data.get("user"))
        self.session_id: str = data["session_id"]
        application_response = await self.http.get("/oauth2/applications/@me")
        application_data = await application_response.json()

        self.application: ClientApplication = ClientApplication(self, application_data)
        if self.overwrite_commands_on_ready:

            command_sorter = defaultdict(list)

            for command in self.commands.values():
                command_payload = {"name": command.name, "type": command.type}

                if command_payload["type"] == 1:
                    command_payload["description"] = command.description
                    command_payload["options"] = [
                        option.to_dict() for option in getattr(command, "options", [])
                    ]
                    if command.name_localizations:
                        command_payload["name_localizations"] = {}
                        for name_localization in command.name_localizations:
                            command_payload["name_localizations"][
                                name_localization
                            ] = command.name_localizations[name_localization.to_dict()]
                    if command.description_localizations:
                        command_payload["description_localizations"] = {}
                        for (
                            description_localization
                        ) in command.description_localizations:
                            command_payload["description_localizations"][
                                description_localization.to_dict()
                            ] = command.description_localizations[
                                description_localization
                            ]

                for guild_id in command.guild_ids or []:
                    command_sorter[guild_id].append(command_payload)
                command_sorter["global"].append(command_payload)

            for guild_id, commands in command_sorter.items():

                if guild_id == "global":
                    await self.application.bulk_overwrite_global_application_commands(
                        commands
                    )
                    continue

                await self.application.bulk_overwrite_guild_application_commands(
                    guild_id, commands
                )
        return None

    async def command_error(self, interaction, error: Exception):
        logger.exception(error)

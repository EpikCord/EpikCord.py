from sys import platform
import asyncio
import async_timeout
from typing import Optional, List, Union
from logging import getLogger
from .exceptions import *

logger = getLogger(__name__)


class EventHandler:
    # Class that'll contain all methods that'll be called when an event is triggered.

    def __init__(self):
        self.events = {}

    async def wait_for(self, event_name: str, check: Optional[callable] = lambda *args, **kwargs: ..., timeout: Optional[Union[float, int]] = None):
        async with async_timeout.timeout(timeout):
            async for event in self.ws:
                event = event.json()
                if event["t"].lower() == event_name.lower():
                    results = self.handle_event(None, event)

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
        if data.get("unavailable"):
            return # The guild is just unavailable

        callback = self.events.get("guild_delete", None)

        if callback:
            await callback(self.guilds.fetch(data["id"])) # Fetch the guild from Cache.

    async def handle_events(self):
        async for event in self.ws:
            event = event.json()
            logger.debug(f"Received {event} from Discord.")

            if event["op"] == self.HELLO:

                self.interval = event["d"]["heartbeat_interval"]

                async def wrapper():
                    while True:
                        await self.heartbeat(False)

                asyncio.create_task(wrapper())
                await self.identify()

                

            elif event["op"] == self.EVENT:
                self.sequence = event["s"]
                logger.info(f"Received event {event['t']}")

                try:
                    await self.handle_event(event["t"], event["d"])
                except Exception as e:
                    logger.exception(f"Error handling event {event['t']}: {e}")

                if self.wait_for_events[event["t"]]:
                    for event in self.wait_for_events[event["t"]]:
                        if event["check"](event["data"]):
                            self.wait_for_events[event["t"]].remove(event["t"])
                            return event["data"]

            elif event["op"] == self.HEARTBEAT:
                # I shouldn't wait the remaining delay according to the docs.
                await self.heartbeat(True)

            elif event["op"] == self.HEARTBEAT_ACK:
                try:
                    self.heartbeats.append(event["d"])
                except AttributeError:
                    self.heartbeats = [event["d"]]

            elif event["op"] == self.RECONNECT:
                await self.reconnect()

            elif event["op"] == self.RESUMED:
                logger.debug("Connection successfully resumed and all proceeding events are new.")

            if event["op"] != self.EVENT:
                logger.debug(f"Received OPCODE: {event['op']}")


        await self.handle_close()

    async def interaction_create(self, data):

        event_func = self.events.get("interaction_create")


        interaction_type = data.get("type")
        def figure_out_interaction_class():
            if interaction_type == 2:
                return ApplicationCommandInteraction(self, data)
            elif interaction_type == 3:
                return MessageComponentInteraction(self, data)
            elif interaction_type == 4:
                return AutoCompleteInteraction(self, data)
            elif interaction_type == 5:
                return ModalSubmitInteraction(self, data)

        interaction = figure_out_interaction_class()

        if interaction.is_ping():
            await self.http.post(f"interactions/{interaction.id}/{interaction.token}/callback", json = {"type": 1})

        elif interaction.is_application_command():
            command_exists = list(filter(lambda item: item.name == interaction.command_name, self.commands))
            option_values = []
            if bool(command_exists): # bool(Filter) returns True every time.
                if interaction.options:
                    for option in interaction.options:
                        option_values.append(option.get("value"))
                await command_exists[0].callback(interaction, *option_values)
        if interaction.is_message_component():
            if self._components.get(interaction.custom_id):
                if interaction.is_button():
                    action_rows = interaction.message.components
                    for component in action_rows[0].components["components"]:
                        if component["custom_id"] == interaction.custom_id:
                            del component["type"]
                            await self._components[interaction.custom_id](interaction, Button(**component))
                            break
                    # for row in action_rows:
                    #     for component in row.components:
                    #         print(component)
                    #         if component.custom_id == interaction.custom_id:
                    #             await self._components[interaction.custom_id](interaction, component)
                    #             return

        if interaction.is_autocomplete():
            for command in self.commands:
                if command.name == interaction.command_name:
                    ...

        if interaction.is_modal_submit():
            action_rows = interaction._components
            component_object_list = []
            for action_row in action_rows:
                for component in action_row.get("components"):
                    component_object_list.append(component["value"]) # TODO: Fix this later, component_object_list is empty ;()
            await self._components.get(interaction.custom_id)(interaction, *component_object_list)

        await event_func(interaction) if event_func else None


    async def handle_event(self, event_name: Optional[str], data: dict):
        event_name = event_name.lower()
        callback = self.get_event_callback(event_name)


        await callback()


    async def get_event_callback(self, event_name: str, internal = False):

        if internal:
            event_callback = getattr(self, event_name) if hasattr(self, event_name) else None
            
        else:
            event_callback = self.events.get(event_name, None)

        if event_callback:
            return event_callback

        return None



    async def channel_create(self, data: dict):
        channel_type: str = data.get("type")
        event_func = None
        try:
            event_func = self.events["channel_create"]
        except KeyError:
            ...

        if channel_type in {0, 1, 5, 6, 10, 11, 12}:

            if event_func:
                await event_func(TextBasedChannel(self, data).to_type())

        elif channel_type == 2:
            if event_func:
                await event_func(VoiceChannel(self, data))

        elif channel_type == 13:
            if event_func:
                await event_func(GuildStageChannel(self, data))

        # if channel_type in (0, 5, 6):
        #     try:
        #         event_func = self.events["channel_create"]
        #     except KeyError:
        #         ...
        #     if event_func:
        #         await event_func(TextBasedChannel(self, channel_data))

        # elif channel_type == 1:
        #     try:
        #         event_func = self.events["dm_channel_create"]
        #         await event_func(DMChannel(self, channel_data))
        #     except KeyError:
        #         pass
        
        # elif channel_type == 2:
        #     try:
        #         event_func = self.events["channel_create"]
        #     except KeyError:
        #         pass    
        #     await event_func(VoiceChannel(self, channel_data))
        
        # elif channel_type == 13:
        #     try:
        #         event_func = self.events["channel_create"]
        #     except KeyError:
        #         pass
        #     await event_func(GuildStageChannel(self, channel_data))
        
        # elif channel_type in (10, 11, 12)
    

    async def message_create(self, data: dict):
        """Event fired when messages are created"""
        if self.events.get("message_create"):
            message = Message(self, data)
            message.channel = Messageable(self, data.get("channel_id"))
            await self.events["message_create"](message)

    async def guild_create(self, data):
        if not data.get("available"): # If it's not available
            self.guilds.add_to_cache(data.get("id"), UnavailableGuild(data))
            return 
            # Don't call the event for an unavailable guild, users expect this to be when they join a guild, not when they get a pre-existing guild that is unavailable.
        else:
            self.guilds.add_to_cache(data.get("id"), Guild(self, data))

        channels =  data.get("channels", [])
        for channel in channels:
            self.channels.add_to_cache(data["id"], self.utils.channel_from_type(channel))

        try:
            event_func = self.events["guild_create"]
        except KeyError:
            return

        await event_func(Guild(self, data))


    def event(self, func):
        func_name = func.__name__.lower()

        if func_name.startswith("on_"):
            func_name = func_name[3:]
        
        self.events[func_name] = func

    async def guild_member_update(self, data):
        ...

    async def ready(self, data: dict):
        self.user: ClientUser = ClientUser(self, data.get("user"))
        self.session_id: str = data["session_id"]
        application_response = await self.http.get("/oauth2/applications/@me")
        application_data = await application_response.json()
        self.application: ClientApplication = ClientApplication(
            self, application_data
            )

        command_sorter = {
            "global": []
        }

        for command in self.commands:
            command_payload = {
                "name": command.name,
                "type": command.type
            }

            if command_payload["type"] == 1:
                command_payload["description"] = command.description
                command_payload["options"] = [option.to_dict() for option in getattr(command, "options", [])]

            if getattr(command, "guild_ids", None):
                for guild_id in command.guild_ids:
                    try:
                        command_sorter[guild_id].append(command_payload)
                    except KeyError:
                        command_sorter[guild_id] = [command_payload]
            else:
                command_sorter["global"].append(command_payload)

        for guild_id, commands in command_sorter.items():

            if guild_id == "global":
                await self.application.bulk_overwrite_global_application_commands(commands)
            else:
                await self.application.bulk_overwrite_guild_application_commands(guild_id, commands)

        try:
            await self.events["ready"]()
        except KeyError:
            return


class WebsocketClient(EventHandler):
    def __init__(self, token: str, intents: int):

        super().__init__()
        self.EVENT = 0
        self.HEARTBEAT = 1
        self.IDENTIFY = 2
        self.PRESENCE_UPDATE = 3
        self.VOICE_STATE_UPDATE = 4
        self.RESUME = 6
        self.RECONNECT = 7
        self.REQUEST_GUILD_MEMBERS = 8
        self.INVALID_SESSION = 9
        self.HELLO = 10
        self.HEARTBEAT_ACK = 11

        self.token = token
        if not token:
            raise TypeError("Missing token.")

        if isinstance(intents, int):
            self.intents = intents
        elif isinstance(intents, Intents):
            self.intents = intents.value

        self.commands = {}
        self._closed = False  # Well nah we're starting closed
        self.heartbeats = []
        self.average_latency = 0

        self.interval = None  # How frequently to heartbeat
        self.session_id = None
        self.sequence = None

    async def change_presence(self, *, presence: Optional[Presence]):
        payload = {
            "op": 3,
            "d": presence.to_dict()
        }
        await self.send_json(payload)

    async def heartbeat(self, forced: Optional[bool] = None):
        if forced:
            return await self.send_json({"op": self.HEARTBEAT, "d": self.sequence or "null"})

        if self.interval:
            await self.send_json({"op": self.HEARTBEAT, "d": self.sequence or "null"})
            await asyncio.sleep(self.interval / 1000)
            logger.debug("Sent a heartbeat!")

    async def request_guild_members(self, guild_id: int, *, query: Optional[str] = None, limit: Optional[int] = None, presences: Optional[bool] = None, user_ids: Optional[List[str]] = None, nonce: Optional[str] = None):
        payload = {
            "op": self.REQUEST_GUILD_MEMBERS,
            "d": {
                "guild_id": guild_id
            }
        }

        if query:
            payload["d"]["query"] = query

        if limit:
            payload["d"]["limit"] = limit

        if presences:
            payload["d"]["presences"] = presences
        
        if user_ids:
            payload["d"]["user_ids"] = user_ids
        
        if nonce:
            payload["d"]["nonce"] = nonce

        await self.send_json(payload)

    async def reconnect(self):
        await self.close()
        self.ws = await self.http.ws_connect("wss://gateway.discord.gg/?v=9&encoding=json")
        await self.send_json({
            "op": self.RECONNECT,
            "d": {
                "token": self.token,
                "session_id": self.session_id,
                "seq": self.sequence
            }
        })
        self._closed = False
        await self.handle_events()

    async def handle_close(self):
        if self.ws.close_code == 4014:
            raise DisallowedIntents(
                "You cannot use privellaged intents with this token, go to the developer portal and allow the privellaged intents needed.")
        elif self.ws.close_code == 1006:
            await self.resume()
        elif self.ws.close_code == 4004:
            raise InvalidToken("The token you provided is invalid.")
        elif self.ws.close_code == 4008:
            raise Ratelimited429(
                "You've been rate limited. Try again in a few minutes.")
        elif self.ws.close_code == 4011:
            raise ShardingRequired("You need to shard the bot.")
        elif self.ws.close_code == 4012:
            raise DeprecationWarning("The gateway you're connecting to is deprecated and does not work, upgrade EpikCord.py.")
        elif self.ws.close_code == 4013:
            raise InvalidIntents("The intents you provided are invalid.")
        elif self.ws.close_code == 4000:
            await self.resume()
        elif self.ws.close_code == 4001:
            logger.critical("EpikCord.py sent an invalid OPCODE to the Gateway. Report this immediately.")
            await self.resume()
        elif self.ws.close_code == 4002:
            logger.critical("EpikCord.py sent an invalid payload to the Gateway. Report this immediately.")
            await self.resume()
        elif self.ws.close_code == 4003:
            logger.critical(f"EpikCord.py has sent a payload prior to identifying. Report this immediately.")
        elif self.ws.close_code == 4005:
            logger.critical("EpikCord.py tried to authenticate again. Report this immediately.")
            await self.resume()
        elif self.ws.close_code == 4007:
            logger.critical("EpikCord.py sent an invalid sequence number. Report this immediately.")
            await self.resume()
        elif self.ws.close_code == 4009:
            logger.critical("Session timed out.")
            await self.resume()
        else:
            raise ClosedWebSocketConnection(f"Connection has been closed with code {self.ws.close_code}")

    async def send_json(self, json: dict):
        await self.ws.send_json(json)
        logger.debug(f"Sent {json} to the Websocket Connection to Discord.")


    async def connect(self):
        self.ws = await self.http.ws_connect("wss://gateway.discord.gg/?v=9&encoding=json")
        self._closed = False
        asyncio.create_task(self.handle_events())

    async def resume(self):
        logger.critical("Reconnecting...")
        await self.connect()
        await self.send_json({
            'op': self.RESUME,
            'd': {
                'seq': self.sequence,
                'session_id': self.session_id,
                'token': self.token
            }
        })
        self._closed = False

    async def identify(self):
        payload = {
            "op": self.IDENTIFY,
            "d": {
                "token": self.token,
                "intents": self.intents,
                "properties": {
                    "$os": platform,
                    "$browser": "EpikCord.py",
                    "$device": "EpikCord.py"
                }
            }
        }
        if self.presence:
            payload["d"]["presence"] = self.presence.to_dict()
        return await self.send_json(payload)

    async def close(self) -> None:
        if self._closed:
            return

        self._closed = True

        # for voice in self.voice_clients:
        #     try:
        #         await voice.disconnect(force=True)
        #     except Exception:
        #         # if an error happens during disconnects, disregard it.
        #         pass

        if self.ws is not None and not self.ws.closed:
            await self.ws.close(code=4000)

        if self.http is not None and not self.http.closed:
            await self.http.close()

        self._closed = True

    def login(self):

        loop = asyncio.get_event_loop()

        async def runner():
            try:
                await self.connect()
            finally:
                if not self._closed:
                    await self.close()

        def stop_loop_on_completion(f: asyncio.Future):
            loop.stop()

        future = asyncio.ensure_future(runner(), loop=loop)
        future.add_done_callback(stop_loop_on_completion)

        try:
            loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            future.remove_done_callback(stop_loop_on_completion)
            self.utils.cleanup_loop(loop)
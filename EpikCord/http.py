import asyncio
import threading
from .application import ClientApplication
from .channel import TextBasedChannel, VoiceChannel, GuildStageChannel
from .errors import DisallowedIntents, InvalidToken, Ratelimited429, InvalidIntents, ClosedWebSocketConnection
from .guild import UnavailableGuild, Guild
from .http import ClientSession
from .intents import Intents
from .interactions import ApplicationCommandInteraction, AutoCompleteInteraction, ModalSubmitInteraction, MessageComponentInteraction
from .message import Message, Messageable
from .member import ClientUser
from EpikCord import logger
from typing import Optional, Any


def _cancel_tasks(loop) -> None:
    tasks = {t for t in asyncio.all_tasks(loop=loop) if not t.done()}

    if not tasks:
        return

    for task in tasks:
        task.cancel()
    logger.debug(f"Cancelled {len(tasks)} tasks")
    loop.run_until_complete(asyncio.gather(*tasks, return_exceptions=True))


def _cleanup_loop(loop) -> None:
    try:
        _cancel_tasks(loop)
        logger.debug("Shutting down async generators.")
        loop.run_until_complete(loop.shutdown_asyncgens())
    finally:
        loop.close()


class RatelimitHandler:
    """
    A class to handle ratelimits from Discord.
    """
    def __init__(self):
        self.ratelimit_buckets: dict = {}
        self.ratelimited: bool = False

    async def process_headers(self, headers: dict):
        """
        Read the headers from a request and then digest it.
        """
        if "X-Ratelimit-Bucket" in headers:

            self.ratelimit_buckets[headers["X-Ratelimit-Bucket"]] = {
                "limit": headers["X-Ratelimit-Limit"],
                "remaining": headers["X-Ratelimit-Remaining"],
                "reset": headers["X-Ratelimit-Reset"]
            }

            if headers.get("retry_after"):
                await self.handle_ratelimit(headers)

    async def handle_ratelimit(self, headers: dict):
        """
        Handles ratelimits from Discord.
        """
  
        self.ratelimited = True
        await asyncio.sleep(headers["retry_after"])
        self.ratelimited = False

    def is_ratelimited(self) -> bool:
        """
        Checks if the client is ratelimited.
        """
        return self.ratelimited


class HTTPClient(ClientSession):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_uri: str = "https://discord.com/api/v9"
        self.ratelimit_handler = RatelimitHandler()

    async def get(self, url, *args, **kwargs):

        if self.ratelimit_handler.is_ratelimited():
            return

        if url.startswith("/"):
            url = url[1:]

        try:
            res = await super().get(f"{self.base_uri}/{url}", *args, **kwargs)
        except:
            await self.ratelimit_handler.process_headers(res.headers)            

        return res

    async def post(self, url, *args, **kwargs):

        if self.ratelimit_handler.is_ratelimited():
            return

        if url.startswith("/"):
            url = url[1:]
        res = await super().post(f"{self.base_uri}/{url}", *args, **kwargs)
        # except:
        #     await self.ratelimit_handler.process_headers(res.headers)

        return res

    async def patch(self, url, *args, **kwargs):

        if self.ratelimit_handler.is_ratelimited():
            return

        if url.startswith("/"):
            url = url[1:]
        try:
            res = await super().patch(f"{self.base_uri}/{url}", *args, **kwargs)
        except:
            await self.ratelimit_handler.process_headers(res.headers)

        return res

    async def delete(self, url, *args, **kwargs):

        if self.ratelimit_handler.is_ratelimited():
            return

        if url.startswith("/"):
            url = url[1:]

        try:
            res = await super().delete(f"{self.base_uri}/{url}", *args, **kwargs)
        except:
            await self.ratelimit_handler.process_headers(res.headers)

        return res

    async def put(self, url, *args, **kwargs):

        if self.ratelimit_handler.is_ratelimited():
            return

        if url.startswith("/"):
            url = url[1:]
        try:
            res = await super().put(f"{self.base_uri}/{url}", *args, **kwargs)
        except:
            await self.ratelimit_handler.process_headers(res.headers)

        return res

    async def head(self, url, *args, **kwargs):

        if self.ratelimit_handler.is_ratelimited():
            return

        if url.startswith("/"):
            url = url[1:]

        try:
            res =  await super().head(f"{self.base_uri}/{url}", *args, **kwargs)
        except:
            await self.ratelimit_handler.process_headers(res.headers)

        return res

class EventHandler:
    # Class that'll contain all methods that'll be called when an event is triggered.

    def __init__(self):
        self.events = {}
        self.wait_for_events = {}
        self.PING: int = 1
        self.PONG: int = 1
        self.CHANNEL_MESSAGE_WITH_SOURCE: int = 4
        self.DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE: int = 5
        self.DEFERRED_UPDATE_MESSAGE: int = 6
        self.UPDATE_MESSAGE: int = 7
        self.APPLICATION_COMMAND_AUTOCOMPLETE_RESULT: int = 8
        self.MODAL: int = 9

    async def handle_events(self):
        async for event in self.ws:
            event = event.json()

            if event["op"] == self.HELLO:

                self.interval = event["d"]["heartbeat_interval"]

                await self.identify()

            elif event["op"] == self.EVENT:
                await self.handle_event(event["t"], event["d"])
                if event["t"] in self.wait_for_events:
                    if self.wait_for_events[event["t"]](): # If the function succeeds, we remove it from the wait_for_events dict and return the results
                        del self.wait_for_events[event["t"]]


            elif event["op"] == self.HEARTBEAT:
                # I shouldn't wait the remaining delay according to the docs.
                await self.heartbeat(True)

            elif event["op"] == self.HEARTBEAT_ACK:
                try:
                    self.heartbeats.append(event["d"])
                except AttributeError:
                    self.heartbeats = [event["d"]]
                self.sequence = event["s"]
            logger.debug(f"Received event {event['t']}")
        await self.handle_close()

    async def wait_for(self, event_name: str, *, check: Optional[Any]):
        self.wait_for_events[event_name] = check

    async def interaction_create(self, data):
        if data.get("type") == self.PING:
            await self.client.http.post(f"/interactions/{data.get('id')}/{data.get('token')}/callback", json = {"type": self.PONG})
        
        event_func = None

        event_func = self.events["interaction_create"]

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

        command_exists = list(filter(lambda item: item["name"] == interaction.command_name, self.commands))

        if bool(command_exists): # bool(Filter) returns True every time.
            await command_exists[0]["callback"](interaction)


        await event_func(interaction)


    async def handle_event(self, event_name: str, data: dict):
        event_name = event_name.lower()

        event_func = None
        try:
            event_func = getattr(self, event_name)
        except AttributeError:
            logger.warning(f"A new event, {event_name}, has been added and EpikCord hasn't added that yet. Open an issue to be the first!")
            return
        await event_func(data)

    async def channel_create(self, data: dict):
        channel_type: str = data.get("type")
        event_func = None
        try:
            event_func = self.events["channel_create"]
        except KeyError:
            ...
        
        if channel_type in (0, 1, 5, 6, 10, 11, 12):
            
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
            logger.info(f"message_create event has been fired, Details: {data}")
            message = Message(self, data)
            message.channel = Messageable(self, data.get("channel_id"))
            await self.events["message_create"](message)

    async def guild_create(self, data):
        if not data.get("available"): # If it's not available
            logger.info(f"guild_create event has been fired, Details: {data}")
            self.guilds.add_to_cache(data.get("id"), UnavailableGuild(data))
            return 
            # Don't call the event for an unavailable guild, users expect this to be when they join a guild, not when they get a pre-existing guild that is unavailable.
        else:
            self.guilds.add_to_cache(data.get("id"), Guild(self, data))

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
        application_response = await self.http.get("/oauth2/applications/@me")
        application_data = await application_response.json()
        self.application: ClientApplication = ClientApplication(
            self, application_data
            )

        def heartbeater():
            loop = asyncio.new_event_loop()
            loop.run_until_complete(self.heartbeat(False))
            loop.run_forever()

        threading._start_new_thread(heartbeater, ())

        command_sorter = {
            "global": []
        }


        for command in self.commands:
            command_payload = {
                "name": command["name"],
                "type": command["type"]
            }

            if command["type"] == 1:
                command_payload["description"] = command["description"]
                command_payload["options"] = [option.to_dict() for option in command["options"]]

            if command.get("guild_id"):
                if command_sorter.get(command["guild_id"]):
                    command_sorter[command["guild_id"]].append(command_payload)
                else:
                    command_sorter[command["guild_id"]] = [command_payload]
            else:
                command_sorter["global"].append(command_payload)

        for guild_id, commands in command_sorter.items():

            if guild_id == "global":
                await self.application.bulk_overwrite_global_application_commands(commands)
            else:
                await self.bulk_overwrite_guild_application_commands(guild_id, commands)

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

    async def heartbeat(self, forced: Optional[bool] = None):
        if forced:
            return await self.send_json({"op": self.HEARTBEAT, "d": self.sequence or "null"})

        if self.interval:
            while True:
                await asyncio.sleep(self.interval / 1000)
                await self.send_json({"op": self.HEARTBEAT, "d": self.sequence or "null"})
                logger.debug("Sent a heartbeat!")

    async def handle_close(self):
        if self.ws.close_code == 4014:
            raise DisallowedIntents(
                "You cannot use privellaged intents with this token, go to the developer portal and allow the privellaged intents needed.")
        elif self.ws.close_code == 4004:
            raise InvalidToken("The token you provided is invalid.")
        elif self.ws.close_code == 4008:
            raise Ratelimited429(
                "You've been rate limited. Try again in a few minutes.")
        elif self.ws.close_code == 4013:
            raise InvalidIntents("The intents you provided are invalid.")
        else:
            raise ClosedWebSocketConnection(f"Connection has been closed with code {self.ws.close_code}")

    async def send_json(self, json: dict):
        try:
            await self.ws.send_json(json)
        except:
            logger.debug(f"Exited with code: {self.ws.close_code}")

    async def connect(self):
        self.ws = await self.http.ws_connect("wss://gateway.discord.gg/?v=9&encoding=json")
        await self.handle_events()
        self._closed = False

    async def resume(self):
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
        await self.send_json({
            "op": self.IDENTIFY,
            "d": {
                "token": self.token,
                "intents": self.intents,
                "properties": {
                    "$os": "linux",
                    "$browser": "EpikCord.py",
                    "$device": "EpikCord.py"
                }
            }
        }
        )

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

        if self.ws is not None:
            if not self.ws.closed:
                await self.ws.close(code=1000)

        if self.http is not None:
            if not self.http.closed:
                await self.http.close()

        self._closed = True

    def login(self):

        loop = asyncio.get_event_loop()

        async def runner():
            try:
                await self.connect()
            finally:
                if self._closed != True:
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
            _cleanup_loop(loop)



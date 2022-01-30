from websocket import WebSocket
from asyncio import get_event_loop
from .slash_command import Subcommand, SubCommandGroup, StringOption, IntegerOption, BooleanOption, UserOption, ChannelOption, RoleOption, MentionableOption, NumberOption
from typing import (
    List,
    Union
)
from asyncio import sleep
from json import loads, dumps
from threading import _start_new_thread

class EventHandler:
    # Class that'll contain all methods that'll be called when an event is triggered.    

    def __init__(self):
        self.events = {}

    def event(self, func):
        def register_event():
            self.events[func.__name__.lower().replace("on_")] = func
        return register_event

    async def ready(self, data: dict):
        pass

    

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

        self.ws = self.http
        self.token = token
        self.intents = intents
        self.interval = None
        self.session_id = None
        self.commands = {}
        self.hearbeats = []
        self.average_latency = 0        
    
    async def heartbeat(self):
        await sleep(self.interval / 1000)
        await self.ws.send_json({"op": self.HEARTBEAT, "d": "null"})
        event = await self.receive_event()
        if event:
            if event["op"] == self.HEARTBEAT_ACK:
                self.heartbeats.append(event["d"])
                self.sequence = event["s"]
        print("Sent heartbeat!")
    
    async def receive_event(self):

        response = await self.ws.receive()
        if response:
            return response.json()
    
    async def handle_event(self, event_name: str, data: dict):
        try:
            await getattr(self, event_name)(data)
        except AttributeError:
            print("A new event has been added and EpikCord hasn't added that yet. Open an issue to be the first!")
        try:
            await self.events[event_name](data)
            print("Ran event!")
        except KeyError:
            pass
    
    
    def command(self, *, name: str, description: str, guild_ids: List[str], options:Union[Subcommand, SubCommandGroup, StringOption, IntegerOption, BooleanOption, UserOption, ChannelOption, RoleOption, MentionableOption, NumberOption]):
        def register_slash_command(func):
            self.commands[func.__name__] = {"callback": func, "name": name, "description": description, "guild_ids": guild_ids, "options": options}
        return register_slash_command

    async def connect(self):
        await self.ws.connect("wss://gateway.discord.gg/?v=9&encoding=json")
        event = await self.receive_event()
        self.interval = event["d"]["heartbeat_interval"]
        await self.ws.send_json({
            "op": self.IDENTIFY,
            "d": {
                "token": self.token,
                "intents": self.intents,
                "properties": {
                    "$os": "linux",
                    "$browser": "EpikCord.py",
                    "$device": "EpikCord.py"
                    },
                }
            }
        )
        await self.receive_event()
    

    def login(self):
        asyncio.get_event_loop().run_forever(self.connect())
from .abc import BaseInteraction
from websocket import WebSocket
from asyncio import run
from .slash_command import Subcommand, SubCommandGroup, StringOption, IntegerOption, BooleanOption, UserOption, ChannelOption, RoleOption, MentionableOption, NumberOption
from typing import (
    List,
    Union
)
from time import sleep
from json import loads, dumps
from threading import _start_new_thread

class WebsocketClient:
    def __init__(self, token: str, intents: int):

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

        self.ws = WebSocket()
        self.token = token
        self.intents = intents
        self.interval = None
        self.session_id = None
        self.events = {}
        self.commands = {}
        self.hearbeats = []
        self.average_latency = 0
        
    async def interaction(self, interaction: BaseInteraction):
        await self.commands[interaction.command_name]["callback"](interaction)
        
    
    def heartbeat(self):
        while True:
            sleep(self.interval / 1000)
            self.ws.send(dumps({"op": self.HEARTBEAT, "d": "null"}))
            event = self.receive_event()
            if event:
                if event["op"] == self.HEARTBEAT_ACK:
                    self.heartbeats.append(event["d"])
                    self.sequence = event["s"]
            print("Sent heartbeat!")
    
    def receive_event(self):
        response = self.ws.recv()
        if response:
            return loads(response)
    
    def handle_event(self, event_name: str, data: dict):
        try:
            function = self.events[event_name]
            run(function(data))
        except KeyError:
            print(f"You have not registered an event handler for {event_name} but still receive the event. Either make a handler or remove the intent to view this event if possible.") # Someone change this to logger

    def infinitely_retreive_events(self):
        while True:
            event = self.receive_event()
            if event:
                if event["op"] == self.EVENT:
                    self.handle_event(event["t"].lower(), event["d"])
                elif event["op"] == self.HEARTBEAT:
                    self.ws.send(dumps({"op": self.HEARTBEAT, "d": self.sequence or "null"}))

    def event(self, func):
        def register_event():
            self.events[func.__name__.lower().replace("on_")] = func
        return register_event
    
    def command(self, *, name: str, description: str, guild_ids: List[str], options:Union[Subcommand, SubCommandGroup, StringOption, IntegerOption, BooleanOption, UserOption, ChannelOption, RoleOption, MentionableOption, NumberOption]):
        def register_slash_command(func):
            self.commands[func.__name__] = {"callback": func, "name": name, "description": description, "guild_ids": guild_ids, "options": options}
        return register_slash_command

    def login(self):
        self.ws.connect("wss://gateway.discord.gg/?v=9&encoding=json")
        event = self.receive_event()
        print(event)
        self.interval = event["d"]["heartbeat_interval"]
        self.ws.send(
            dumps({
            "op": self.IDENTIFY,
            "d": {
                "token": self.token,
                "intents": self.intents,
                "properties": {
                    "$os": "linux",
                    "$browser": "EpikCord",
                    "$device": "EpikCord"
                    },
                }
            })
        )
        _start_new_thread(self.heartbeat, ())
        
        self.infinitely_retreive_events()
from websocket import WebSocket
from asyncio import run
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
        self.hearbeats = []
        self.average_latency = 0
        
    
    def heartbeat(self):
        while True:
            print("Sleeping")
            sleep(self.interval / 1000)
            print("Sending heartbeat")
            self.ws.send(dumps({"op": self.HEARTBEAT, "d": "null"}))
            event = self.receive_event()
            if event:
                if event["op"] == self.HEARTBEAT_ACK:
                    self.heartbeats.append(event["d"])
            print("Sent heartbeat!")
    
    def receive_event(self):
        response = self.ws.recv()
        if response:
            return loads(response)
    
    def handle_event(self, event_name: str):
        try:
            run(self.events[event_name]())
        except KeyError:
            print(f"You have not registered an event handler for {event_name} but still receive the event. Either make a handler or remove the intent to view this event if possible.") # Someone change this to logger

    def infinitely_retreive_events(self):
        while True:
            event = self.receive_event()
            if event:
                if event["op"] == self.EVENT:
                    self.handle_event(event["t"].lower())
                
    def event(self, func):
        self.events[func.__name__.lower()] = func

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
from aiohttp import ClientSession
from .application import Application
import asyncio
from .user import ClientUser

class EventHandler:
    # Class that'll contain all methods that'll be called when an event is triggered.    

    def __init__(self):
        self.events = {}

    def event(self, func):
        def register_event():
            self.events[func.__name__.lower().replace("on_")] = func
        return register_event

    async def ready(self, data: dict):
        self.user: ClientUser = ClientUser(data["user"])
        self.application: Application = Application(data["application"])
    

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
        self.intents = intents
        self.session = ClientSession()
        self.commands = {}
        self.hearbeats = []
        self.average_latency = 0        

        self.interval = None # How frequently to heartbeat
        self.session_id = None
        self.sequence = None

    async def heartbeat(self):
        await asyncio.sleep(self.interval / 1000)
        await self.ws.send_json({"op": self.HEARTBEAT, "d": "null"})
        event = await self.receive_event()
        if event:
            if event["op"] == self.HEARTBEAT_ACK:
                self.heartbeats.append(event["d"])
                self.sequence = event["s"]
        print("Sent heartbeat!")
    
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
    
    async def send_json(self, json: dict):
        await self.ws.send_json(json)

    async def connect(self):
        async with self.session.ws_connect("wss://gateway.discord.gg/?v=9&encoding=json") as ws:
            self.ws = ws

            asyncio.create_task(self.heartbeat())

            async for event in ws:

                event = event.json()

                if event["op"] == self.HELLO:

                    self.interval = event["d"]["heartbeat_interval"]

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
                elif event["op"] == self.EVENT:
                    await self.handle_event(event["t"], event["d"])

                elif event["op"] == self.HEARTBEAT_ACK:
                    self.heartbeats.append(event["d"])
                    self.sequence = event["s"]

    async def resume(self):
        await self.send_json({
            'op': self.RESUME,
            'd': {
                'seq': self.sequence,
                'session_id': self.session_id,
                'token': self.token
            }
        })

    def login(self):
        try:
            asyncio.run(self.connect())
        except KeyboardInterrupt:
            exit()

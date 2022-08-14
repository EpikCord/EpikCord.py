from __future__ import annotations
import asyncio
from typing import Optional, List, TYPE_CHECKING
from logging import getLogger
from .components import ActionRow
from importlib.util import find_spec
from abc import abstractmethod
import socket
from aiohttp import ClientWebSocketResponse
import struct
from .close_event_codes import GatewayCECode
from .exceptions import ClosedWebSocketConnection
from .opcodes import VoiceOpcode, GatewayOpcode
import asyncio

logger = getLogger("EpikCord.channels")

_NACL = find_spec("nacl")


if _NACL:
    import nacl

else:
    logger.warning(
        "The PyNacl library was not found, so voice is not supported."
        " Please install it by doing ``pip install PyNaCl``"
        " If you want voice support"
    )


if TYPE_CHECKING:
    from EpikCord import Message, File, AllowedMention, Check, VoiceChannel

class TypingContextManager:
    def __init__(self, client, channel_id):
        self.typing: asyncio.Task = None
        self.client = client
        self.channel_id: str = channel_id

    async def start_typing(self):

        await self.client.http.post(f"/channels/{self.channel_id}/typing")
        asyncio.get_event_loop().call_later(10, self.start_typing)

    async def __aenter__(self):
        self.typing = asyncio.create_task(self.start_typing())

    async def __aexit__(self):
        self.typing.cancel()

class Messageable:
    def __init__(self, client, channel_id: str):
        if isinstance(channel_id, (int, str)):
            self.id: str = channel_id
        elif isinstance(channel_id, dict):
            self.id: str = channel_id.get("id")
        else:
            raise TypeError(f"Expected str, int or dict, got {type(channel_id)}")

        self.client = client

    async def fetch_messages(
        self,
        *,
        around: Optional[str] = None,
        before: Optional[str] = None,
        after: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> List[Message]:
        from EpikCord import Message

        response = await self.client.http.get(
            f"channels/{self.id}/messages",
            params={"around": around, "before": before, "after": after, "limit": limit},
        )
        data = await response.json()
        return [Message(self.client, message) for message in data]

    async def fetch_message(self, *, message_id: str) -> Message:
        from EpikCord import Message

        response = await self.client.http.get(
            f"channels/{self.id}/messages/{message_id}"
        )
        data = await response.json()
        return Message(self.client, data)

    async def send(
        self,
        content: Optional[str] = None,
        *,
        embeds: Optional[List[dict]] = None,
        components: List[ActionRow] = None,
        tts: Optional[bool] = False,
        allowed_mention: AllowedMention = None,
        sticker_ids: Optional[List[str]] = None,
        attachments: List[File] = None,
        suppress_embeds: bool = False,
    ) -> Message:
        from EpikCord import Message

        payload = self.client.utils.filter_values(
            {
                "content": content,
                "embeds": [embed.to_dict() for embed in embeds],
                "components": [component.to_dict() for component in components],
                "tts": tts,
                "allowed_mentions": allowed_mention.to_dict(),
                "sticker_ids": sticker_ids,
                "attachments": [attachment.to_dict() for attachment in attachments],
            }
        )

        if suppress_embeds:
            payload["suppress_embeds"] = 1 << 2

        response = await self.client.http.post(
            f"channels/{self.id}/messages", json=payload
        )
        data = await response.json()
        return Message(self.client, data)

    async def typing(self) -> TypingContextManager:
        return TypingContextManager(self.client, self.id)

class BaseCommand:
    def __init__(self, checks: Optional[List[Check]]):
        self.checks: List[Check] = checks

    def is_slash_command(self):
        return self.type == 1

    def is_user_command(self):
        return self.type == 2

    def is_message_command(self):
        return self.type == 3

    @property
    @abstractmethod
    def type(self):
        ...

class BaseChannel:
    def __init__(self, client, data: dict):
        self.id: str = data.get("id")
        self.client = client
        self.type = data.get("type")

class Connectable:
    def __init__(
        self,
        client,
        *,
        guild_id: Optional[str] = None,
        channel_id: Optional[str] = None,
        channel: Optional[VoiceChannel] = None,
    ):
        self.client = client
        self.guild_id = channel.guild.id
        self.channel_id = channel.id
        self._closed = True

        self.token: Optional[str] = None
        self.session_id: Optional[str] = None
        self.endpoint: Optional[str] = None
        self.socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setblocking(False)
        self.ws: Optional[ClientWebSocketResponse] = None

        self.heartbeat_interval: Optional[int] = None
        self.server_ip: Optional[str] = None
        self.server_port: Optional[int] = None
        self.ssrc: Optional[int] = None
        self.mode: Optional[List[str]] = None
        self.secret_key: Optional[str] = None

        self.ip: Optional[str] = None
        self.port: Optional[int] = None

    async def connect(
        self, muted: Optional[bool] = False, deafened: Optional[bool] = False
    ):
        await self.client.send_json(
            {
                "op": GatewayOpcode.VOICE_STATE_UPDATE,
                "d": {
                    "guild_id": self.guild_id,
                    "channel_id": self.channel_id,
                    "self_mute": muted,
                    "self_deaf": deafened,
                },
            }
        )
        voice_state_update_coro = asyncio.create_task(
            self.client.wait_for("voice_state_update")
        )
        if not self.client.intents.voice_states:
            raise ValueError(
                "You must have the `voice_states` intent enabled to use "
                "this otherwise we never get the session_id."
            )

        voice_server_update_coro = asyncio.create_task(
            self.client.wait_for(
                "voice_server_update", check=lambda data: data.get("endpoint")
            )
        )
        events, _ = await asyncio.wait(
            [voice_state_update_coro, voice_server_update_coro]
        )
        from EpikCord import VoiceState

        for event in events:
            if isinstance(event.result(), VoiceState):  # If it's the VoiceState
                self.session_id = event.result().session_id
            elif isinstance(event.result(), dict):  # If it's a VoiceServerUpdate
                self.token = event.result()["token"]
                self.endpoint = event.result()["endpoint"]

        await self._connect_ws()

    async def _connect_ws(self):
        wss = "" if self.endpoint.startswith("wss://") else "wss://"
        self.ws = await self.client.http.ws_connect(f"{wss}{self.endpoint}?v=4")
        return await self.handle_events()

    async def handle_events(self):
        async for event in self.ws:
            event = event.json()
            if event["op"] == VoiceOpcode.HELLO:
                await self.handle_hello(event["d"])

            elif event["op"] == VoiceOpcode.READY:
                await self.handle_ready(event["d"])

        await self.handle_close()

    async def handle_close(self):
        self._closed = True
        if self.ws.close_close == GatewayCECode.UnknownOpcode:
            raise ClosedWebSocketConnection(
                "EpikCord has sent an invalid OpCode to the Voice WebSocket."
                " Report this at https://github.com/EpikCord/EpikCord.py/issues"
            )
        elif self.ws.close_code == GatewayCECode.DecodeError:
            raise ClosedWebSocketConnection(
                "EpikCord has sent an invalid identify to the Voice WebSocket."
                " Report this at https://github.com/EpikCord/EpikCord.py/issues"
            )
        elif self.ws.close_code == GatewayCECode.NotAuthenticated:
            raise ClosedWebSocketConnection(
                "EpikCord has sent a payload before identifying to the Voice Websocket."
                " Report this at https://github.com/EpikCord/EpikCord.py/issues"
            )
        elif self.ws.close_code == GatewayCECode.AuthenticationFailed:
            raise ClosedWebSocketConnection(
                "EpikCord sent an invalid token to the Voice Websocket."
                " Report this at https://github.com/EpikCord/EpikCord.py/issues"
            )
        elif self.ws.close_code == GatewayCECode.AlreadyAuthenticated:
            raise ClosedWebSocketConnection(
                "EpikCord sent more than one identify payload."
                " Report this at https://github.com/EpikCord/EpikCord.py/issues"
            )
        elif self.ws.close_code == GatewayCECode.SessionTimedOut:

            raise ClosedWebSocketConnection("The session is no longer valid.")

    async def handle_hello(self, data: dict):
        self.heartbeat_interval = data["heartbeat_interval"]
        await self.identify()

        async def wrapper():
            while True:
                await self.heartbeat()
                await asyncio.sleep(self.heartbeat_interval / 1000)

        loop = asyncio.get_event_loop()
        loop.create_task(wrapper())

    async def handle_ready(self, event: dict):
        self.ssrc: int = event["ssrc"]
        self.mode = event["modes"][0]  # Always has one mode, and I can use any.
        self.server_ip: str = event["ip"]
        self.server_port: int = event["port"]

    async def handle_session_description(self, event: dict):
        self.secret_key: str = event["d"]["secret_key"]

    async def identify(self):
        return await self.send_json(
            {
                "op": VoiceOpcode.IDENTIFY,
                "d": {
                    "server_id": self.guild_id,
                    "user_id": self.client.user.id,
                    "session_id": self.session_id,
                    "token": self.token,
                },
            }
        )

    async def select_protocol(self):
        await self.send_json(
            {
                "op": VoiceOpcode.SELECT_PROTOCOL,
                "d": {
                    "protocol": "udp",  # I don't understand UDP tbh
                    "data": {"address": self.ip, "port": self.port, "mode": self.mode},
                },
            }
        )

    async def send_json(self, json, *args, **kwargs):
        await self.ws.send_json(json, *args, **kwargs)
        logger.info(f"Sent {json} to Voice Websocket {self.endpoint}")

    async def heartbeat(self):
        heartbeat_nonce = nacl.utils.random(nacl.secret.SecretBox.NONCE_SIZE)
        return await self.send_json({"op": VoiceOpcode.HEARTBEAT, "d": heartbeat_nonce})

    async def discover_ip(self):
        udp_packet: bytearray = bytearray(70)
        struct.pack_into(">H", udp_packet, 0, 1)  # Request. At the 0th Index, write 0x1
        struct.pack_into(">H", udp_packet, 2, 70)  # Length of the packet.
        struct.pack_into(">I", udp_packet, 4, self.ssrc)
        self.socket.sendto(udp_packet, (self.server_ip, self.server_port))
        ip_data = await asyncio.get_event_loop().sock_recv(self.socket, 70)
        # type + length = 4
        # We need to start at index 4 to get the address and ignore the type and length
        ip_end = ip_data.index(0, 4)
        self.ip = ip_data[4:ip_end].decode("ascii")
        self.port = struct.unpack_from(">H", ip_data, len(ip_data) - 2)[0]



__all__ = ("Messageable", "BaseCommand", "BaseChannel", "TypingContextManager", "Connectable")

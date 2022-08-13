from __future__ import annotations
from time import perf_counter_ns
from ..exceptions import (
    InvalidIntents,
    InvalidToken,
    ShardingRequired,
    Ratelimited429,
    DisallowedIntents,
    InvalidToken,
    ClosedWebSocketConnection,
)
import asyncio
from sys import platform
from ..close_event_codes import GatewayCECode
from ..opcodes import GatewayOpcode
from typing import Optional, List, TYPE_CHECKING
from logging import getLogger
from .event_handler import EventHandler

if TYPE_CHECKING:
    from EpikCord import Presence

logger = getLogger(__name__)


class WebsocketClient(EventHandler):
    def __init__(self, token: str, intents: int):
        super().__init__()
        from EpikCord import Intents

        self.token = token
        if not token:
            raise TypeError("Missing token.")

        if isinstance(intents, int):
            self.intents = Intents(intents)
        elif isinstance(intents, Intents):
            self.intents = intents

        self._closed = True
        self.heartbeats = []

        self.interval = None  # How frequently to heartbeat
        self.session_id = None
        self.sequence = None

    async def change_presence(self, *, presence: Optional[Presence]):
        payload = {"op": GatewayOpcode.PRESENCE_UPDATE, "d": presence.to_dict()}
        await self.send_json(payload)

    async def heartbeat(self, forced: Optional[bool] = None):
        if forced:
            return await self.send_json(
                {"op": GatewayOpcode.HEARTBEAT, "d": self.sequence or "null"}
            )

        if self.interval:
            await self.send_json(
                {"op": GatewayOpcode.HEARTBEAT, "d": self.sequence or "null"}
            )
            self.heartbeat_time = perf_counter_ns()
            await asyncio.sleep(self.interval / 1000)
            logger.debug("Sent a heartbeat!")

    async def request_guild_members(
        self,
        guild_id: int,
        *,
        query: Optional[str] = None,
        limit: Optional[int] = None,
        presences: Optional[bool] = None,
        user_ids: Optional[List[str]] = None,
        nonce: Optional[str] = None,
    ):
        payload = {
            "op": GatewayOpcode.REQUEST_GUILD_MEMBERS,
            "d": {"guild_id": guild_id},
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
        await self.connect()
        await self.identify()
        await self.resume()

    async def handle_close(self):
        if self.ws.close_code == GatewayCECode.DisallowedIntents:
            raise DisallowedIntents(
                "You cannot use privileged intents with this token, go to "
                "the developer portal and allow the privileged intents "
                "needed. "
            )
        elif self.ws.close_code == 1006:
            await self.resume()
        elif self.ws.close_code == GatewayCECode.AuthenticationFailed:
            raise InvalidToken("The token you provided is invalid.")
        elif self.ws.close_code == GatewayCECode.RateLimited:
            raise Ratelimited429(
                "You've been rate limited. Try again in a few minutes."
            )
        elif self.ws.close_code == GatewayCECode.ShardingRequired:
            raise ShardingRequired("You need to shard the bot.")
        elif self.ws.close_code == GatewayCECode.InvalidAPIVersion:
            raise DeprecationWarning(
                "The gateway you're connecting to is deprecated and does not "
                "work, upgrade EpikCord.py. "
            )
        elif self.ws.close_code == GatewayCECode.InvalidIntents:
            raise InvalidIntents("The intents you provided are invalid.")
        elif self.ws.close_code == GatewayCECode.UnknownError:
            await self.resume()
        elif self.ws.close_code == GatewayCECode.UnknownOpcode:
            logger.critical(
                "EpikCord.py sent an invalid OPCODE to the Gateway. "
                "Report this immediately. "
            )
            await self.resume()
        elif self.ws.close_code == GatewayCECode.DecodeError:
            logger.critical(
                "EpikCord.py sent an invalid payload to the Gateway."
                " Report this immediately. "
            )
            await self.resume()
        elif self.ws.close_code == GatewayCECode.NotAuthenticated:
            logger.critical(
                "EpikCord.py has sent a payload prior to identifying."
                " Report this immediately. "
            )

        elif self.ws.close_code == GatewayCECode.AlreadyAuthenticated:
            logger.critical(
                "EpikCord.py tried to authenticate again." " Report this immediately. "
            )
            await self.resume()
        elif self.ws.close_code == GatewayCECode.InvalidSequence:
            logger.critical(
                "EpikCord.py sent an invalid sequence number."
                " Report this immediately."
            )
            await self.resume()
        elif self.ws.close_code == GatewayCECode.SessionTimeout:
            logger.critical("Session timed out.")
            await self.resume()
        else:
            raise ClosedWebSocketConnection(
                f"Connection has been closed with code {self.ws.close_code}"
            )

    async def send_json(self, json: dict):
        await self.ws.send_json(json)
        logger.debug(f"Sent {json} to the Websocket Connection to Discord.")

    async def connect(self):
        res = await self.http.get("/gateway")
        data = await res.json()
        url = data["url"]

        self.ws = await self.http.ws_connect(
            f"{url}?v=10&encoding=json&compress=zlib-stream"
        )
        self._closed = False
        await self.handle_events()

    async def resume(self):
        logger.critical("Reconnecting...")

        await self.connect()
        await self.send_json(
            {
                "op": GatewayOpcode.RESUME,
                "d": {
                    "seq": self.sequence,
                    "session_id": self.session_id,
                    "token": self.token,
                },
            }
        )

        self._closed = False

    async def identify(self):
        payload = {
            "op": GatewayOpcode.IDENTIFY,
            "d": {
                "token": self.token,
                "intents": self.intents.value,
                "properties": {
                    "os": platform,
                    "browser": "EpikCord.py",
                    "device": "EpikCord.py",
                },
            },
        }

        if self.presence:
            payload["d"]["presence"] = self.presence.to_dict()

        return await self.send_json(payload)

    async def close(self) -> None:
        if self._closed:
            return

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

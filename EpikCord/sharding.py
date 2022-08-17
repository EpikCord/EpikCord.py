import asyncio
from sys import platform
from typing import List, Optional, Union

from .client import (
    ClientApplication,
    ClientUser,
    EventHandler,
    HTTPClient,
    WebsocketClient,
)
from .flags import Intents
from .opcodes import GatewayOpcode
from .presence import Presence
from .utils import Utils


class Shard(WebsocketClient):
    def __init__(
        self,
        token: str,
        intents: Intents,
        shard_id,
        number_of_shards,
        presence: Optional[Presence] = None,
        discord_endpoint: str = "https://discord.com/api/v10",
    ):
        super().__init__(token, intents, presence, discord_endpoint)
        self.shard_id = [shard_id, number_of_shards]

    async def ready(self, data: dict):
        self.user: ClientUser = ClientUser(self, data["user"])
        self.session_id: str = data["session_id"]
        application_response = await self.http.get("/oauth2/applications/@me")
        application_data = await application_response.json()
        self.application: ClientApplication = ClientApplication(self, application_data)

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
                "shard": str(self.shard_id),
            },
        }

        if self.presence:
            payload["d"]["presence"] = self.presence.to_dict()

        await self.send_json(payload)

    async def reconnect(self):
        await self.close()
        await self.connect()
        await self.identify()
        await self.resume()


class ShardManager(EventHandler):
    def __init__(
        self,
        token: str,
        intents: Intents,
        *,
        shards: Optional[int] = None,
        overwrite_commands_on_ready: bool = False,
        discord_endpoint: Optional[str] = None,
        presence: Optional[Presence] = None,
    ):
        super().__init__()
        self.token: str = token
        self.overwrite_commands_on_ready: bool = overwrite_commands_on_ready
        from EpikCord import __version__

        self.http: HTTPClient = HTTPClient(
            headers={
                "Authorization": f"Bot {token}",
                "User-Agent": f"DiscordBot (https://github.com/EpikCord/EpikCord.py {__version__})",
            }
        )
        self.intents: Intents = (
            intents if isinstance(intents, Intents) else Intents(intents)  # type: ignore
        )
        self.desired_shards: Optional[int] = shards
        self.shards: List[Shard] = []
        self.presence: Optional[Presence] = presence
        self.discord_endpoint: Optional[str] = discord_endpoint
        super().__init__()

    def run(self):
        async def wrapper():
            endpoint_data = await self.http.get("/gateway/bot")  # ClientResponse
            endpoint_data = await endpoint_data.json()  # Dict

            max_concurrency = endpoint_data["session_start_limit"]["max_concurrency"]

            shards = self.desired_shards

            if not shards:
                shards = endpoint_data["shards"]

            for shard_id in range(shards):
                self.shards.append(
                    Shard(
                        self.token,
                        self.intents,
                        shard_id,
                        shards,
                        self.presence,
                        self.discord_endpoint,
                    )
                )

            current_iteration = 0  # The current shard_id we've run

            for shard in self.shards:
                shard.events = self.events
                coro = shard.wait_for("ready")
                await shard.login()
                await coro()

                current_iteration += 1

                if current_iteration == max_concurrency:
                    await asyncio.sleep(5)
                    current_iteration = 0  # Reset it

            if self.overwrite_commands_on_ready:
                for shard in self.shards:
                    await Utils(shard).override_commands()

        loop = asyncio.get_event_loop()
        loop.run_until_complete(wrapper())


__all__ = ("Shard", "ShardManager")

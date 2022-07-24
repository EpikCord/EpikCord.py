from logging import getLogger
from collections import deque
from typing import (
    Optional,
    List
)
from ..managers import GuildManager, ChannelManager

from EpikCord import Section


logger = getLogger(__name__)

class Client(WebsocketClient, CommandHandler):
    def __init__(
        self,
        token: str,
        intents: int = 0,
        *,
        status: Optional[Status] = None,
        activity: Optional[Activity] = None,
        overwrite_commands_on_ready: Optional[bool] = False,
        discord_endpoint: str = "https://discord.com/api/v10",
    ):
        super().__init__(token, intents)
        self.overwrite_commands_on_ready: bool = overwrite_commands_on_ready
        self.guilds: GuildManager = GuildManager(self)
        self.channels: ChannelManager = ChannelManager(self)
        self.presence: Presence = Presence(status=status, activity=activity)
        self._components = {}

        self.http: HTTPClient = HTTPClient(
            headers={
                "Authorization": f"Bot {token}",
                "User-Agent": f"DiscordBot (https://github.com/EpikCord/EpikCord.py {__version__})",
            },
            discord_endpoint=discord_endpoint,
        )

        self.utils = Utils(self)
        self.latencies = deque(maxlen=5)
        self.user: ClientUser = None
        self.application: Optional[ClientApplication] = None
        self.sections: List[Section] = []

    @property
    def latency(self):
        return self.discord_latency

    @property
    def average_latency(self):
        return sum(self.latencies) / len(self.latencies)

    def add_check(self, check: "Check"):
        def wrapper(command_callback):
            command = list(
                filter(lambda c: c.callback == command_callback, self.commands.values())
            )
            command[0].checks.append(check)

        return wrapper

    def load_section(self, section: Section):

        for event in section._events.values():
            self.events[event.name] = event.callback

        for command in section._commands.values():
            self.commands[command.name] = command

        logger.info(f"Loaded Section {section.__name__}")

    def load_sections_from_file(self, filename: str):
        sections = import_module(filename)

        for possible_section in sections.__dict__.values():
            if issubclass(possible_section, Section):
                self.load_section(possible_section)
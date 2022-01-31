from typing import (
    List,
    Union
)
from .slash_command import Subcommand, SubCommandGroup, StringOption, IntegerOption, BooleanOption, UserOption, ChannelOption, RoleOption, MentionableOption, NumberOption
from .exceptions import InvalidArgumentType
from .user import ClientUser
from .section import Section
from .websocket import WebsocketClient
from .application import Application, ApplicationCommand
from aiohttp import ClientSession

class HTTPClient:
    def __init__(self, *args, **kwargs):
        self.session = ClientSession(*args, **kwargs)
        self.base_uri: str = "https://discord.com/api/v9"

    async def get(self, url, *args, **kwargs):
        if url.startswith("/"):
            url = url[1:]
        return await self.session.get(f"{self.base_uri}{url}", *args, **kwargs)

    async def post(self, url, *args, **kwargs):
        if url.startswith("/"):
            url = url[1]
        return await self.session.post(f"{self.base_uri}{url}", *args, **kwargs)

    async def patch(self, url, *args, **kwargs):
        if url.startswith("/"):
            url = url[1:]
        return await self.session.patch(f"{self.base_uri}{url}", *args, **kwargs)

    async def delete(self, url, *args, **kwargs):
        if url.startswith("/"):
            url = url[1:]
        return await self.session.delete(f"{self.base_uri}{url}", *args, **kwargs)

    async def put(self, url, *args, **kwargs):
        if url.startswith("/"):
            url = url[1:]
        return await self.session.put(f"{self.base_uri}{url}", *args, **kwargs)

    async def head(self, url, *args, **kwargs):
        if url.startswith("/"):
            url = url[1:]
        return await self.session.head(f"{self.base_uri}{url}", *args, **kwargs)


class Client(WebsocketClient):

    def __init__(self, token: str, intents: int = 0, **options):
        super().__init__(token, intents)
        
        self.commands: List[ApplicationCommand] = []
        
        self.options: dict = options

        self.http = HTTPClient(
            headers = {"Authorization": f"Bot {token}"}
            )
        self.user: ClientUser = None
        self.application: Application = Application(self, self.user)

    def command(self, *, name: str, description: str, guild_ids: List[str], options: Union[Subcommand, SubCommandGroup, StringOption, IntegerOption, BooleanOption, UserOption, ChannelOption, RoleOption, MentionableOption, NumberOption]):
        def register_slash_command(func):
            self.commands[func.__name__] = {"callback": func, "name": name, "description": description, "guild_ids": guild_ids, "options": options}
        return register_slash_command

    def add_section(self, section: Section):
        if not isinstance(section, Section):
            raise InvalidArgumentType("You must pass in a class that inherits from the Section class.")
        for name, command_object in section.commands:
            self.commands[name] = command_object

        for event_name, event_func in section.events:
            self.events[event_name.lower().replace("on_")] = event_func
        
        # Successfully extracted all the valuable stuff from the section        
# class ClientGuildMember(Member):
#     def __init__(self, client: Client,data: dict):
#         super().__init__(data)
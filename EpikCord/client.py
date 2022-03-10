from .application import Application
from .errors import InvalidArgumentType
from .http import WebsocketClient, HTTPClient
from .slash import AnyOption
from .member import ClientUser
from .managers.guilds_manager import GuildManager
from EpikCord import __version__
from typing import Optional, List


class Status:
    def __init__(self, status: str):
        setattr(self, "status", status)

class AllowedMention:
    def __init__(self, allowed_mentions: List[str], replied_user: bool, roles: List[str], users: List[str]):
        self.data = {}
        self.data["parse"] = allowed_mentions
        self.data["replied_user"] = replied_user
        self.data["roles"] = roles
        self.data["users"] = users
        return self.data


class Activity:
    """_summary_
    Represents an Discord Activity object.
    :param name: The name of the activity.
    :param type: The type of the activity.
    :param url: The url of the activity (if its a stream).
    
    """
    def __init__(self, *, name: str, type: int, url: Optional[str] = None):
        self.name = name
        self.type = type
        self.url = url

    def to_dict(self):
        """Returns activity class as dict

        Returns:
            dict: returns :class:`dict` of :class:`activity`
        """
        return {
            "name": self.name,
            "type": self.type,
            "url": self.url
        }



class Client(WebsocketClient):
    def __init__(self, token: str, intents: int = 0):
        super().__init__(token, intents)

        self.commands: List[dict] = [] # TODO: Need to change this to a Class Later
        self.guilds: GuildManager = GuildManager(self)

        self.http = HTTPClient(
            # raise_for_status = True,
            headers = {
                "Authorization": f"Bot {token}",
                "User-Agent": f"DiscordBot (https://github.com/EpikCord/EpikCord.py {__version__})"
            }
        )


        self.user: ClientUser = None
        self.application: Application = None
        self.sections: List[Section] = []

    def command(self, *, name: str, description: str, guild_ids: Optional[List[str]] = [], options: Optional[AnyOption] = []):
        def register_slash_command(func):

            self.commands.append({
                "callback": func,
                "name": name,
                "description": description,
                "guild_ids": guild_ids,
                "options": options,
                "type": 1
            })
        return register_slash_command

    def user_command(self, *, name: str, description: str, guild_ids: Optional[List[str]] = []):
        def register_slash_command(func):
            self.commands.append({
                "callback": func,
                "name": name,
                "description": description,
                "guild_ids": guild_ids,
                "type": 2
            })
        return register_slash_command

    def message_command(self, *, name: str, description: str, guild_ids: Optional[List[str]] = []):
        def register_slash_command(func):

            self.commands.append({
                "callback": func,
                "name": name,
                "description": description,
                "guild_ids": guild_ids,
                "type": 3
            })
        return register_slash_command

    def add_section(self, section: Section):
        if not isinstance(section, Section):
            raise InvalidArgumentType("You must pass in a class that inherits from the Section class.")

        for name, command_object in section.commands:
            self.commands[name] = command_object

        for event_name, event_func in section.events:
            self.events[event_name.lower()] = event_func
        self.sections.append(section)

        # Successfully extracted all the valuable stuff from the section
# class ClientGuildMember(Member):
#     def __init__(self, client: Client,data: dict):
#         super().__init__(data)

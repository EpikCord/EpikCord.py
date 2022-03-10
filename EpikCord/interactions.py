from .embed import Embed
from .member import GuildMember, User
from .ext.components import MessageButton, MessageSelectMenu, MessageTextInput
from typing import Optional, List, Union

class BaseInteraction:
    def __init__(self, client, data: dict):
        self.id: str = data.get("id")
        self.client = client
        self.type: int = data.get("type")
        self.application_id: int = data.get("application_id")
        self.data: Optional[dict] = data.get("data")
        self.guild_id: Optional[str] = data.get("guild_id")
        self.channel_id: Optional[str] = data.get("channel_id")
        self.member: Optional[GuildMember] = GuildMember(client, data.get("member")) if data.get("member") else None
        self.user: Optional[User] = User(client, data.get("user")) if data.get("user") else None
        self.token: str = data.get("token")
        self.version: int = data.get("version")
        self.locale: Optional[str] = data.get("locale")
        self.guild_locale: Optional[str] = data.get("guild_locale")

    def is_application_command(self):
        return self.type == 2

    def is_message_component(self):
        return self.type == 3

    def is_autocomplete(self):
        return self.type == 4
    
    def is_modal_submit(self):
        return self.type == 5

    async def reply(self, *, tts: bool = False, content: Optional[str] = None, embeds: Optional[List[Embed]] = None, allowed_mentions = None, flags: Optional[int] = None, components: Optional[List[Union[MessageButton, MessageSelectMenu, MessageTextInput]]] = None, attachments: Optional[List[Attachment]] = None) -> None:

        message_data = {
            "tts": tts
        }

        if content:
            message_data["content"] = content
        if embeds:
            message_data["embeds"] = [embed.to_dict() for embed in embeds]
        if allowed_mentions:
            message_data["allowed_mentions"] = allowed_mentions.to_dict()
        if flags:
            message_data["flags"] = flags
        if components:
            message_data["components"] = [component.to_dict() for component in components]
        if attachments:
            message_data["attachments"] = [attachment.to_dict() for attachment in attachments]

        payload = {
            "type": 4,
            "data": message_data
        }

        await self.client.http.post(f"/interactions/{self.id}/{self.token}/callback", json = payload)


    async def defer(self):
        payload = {
            "type": 5
        }
        response = await self.client.http.post(f"/interactions/{self.id}/{self.token}/callback", json = payload)
        return await response.json()

    async def fetch_reply(self):
        response = await self.client.http.get(f"/webhooks/{self.application_id}/{self.token}/messages/@original")
        return await response.json()

    async def edit_reply(self, *, tts: bool = False, content: Optional[str] = None, embeds: Optional[List[Embed]] = None, allowed_mentions = None, flags: Optional[int] = None, components: Optional[List[Union[MessageButton, MessageSelectMenu, MessageTextInput]]] = None, attachments: Optional[List[Attachment]] = None):

        message_data = {
            "tts": tts
        }

        if content:
            message_data["content"] = content
        if embeds:
            message_data["embeds"] = [embed.to_dict() for embed in embeds]
        if allowed_mentions:
            message_data["allowed_mentions"] = allowed_mentions.to_dict()
        if flags:
            message_data["flags"] = flags
        if components:
            message_data["components"] = [component.to_dict() for component in components]
        if attachments:
            message_data["attachments"] = [attachment.to_dict() for attachment in attachments]


        response = await self.client.http.patch(f"/webhooks/{self.application_id}/{self.token}/messages/@original", json = payload)
        return await response.json()

    async def delete_reply(self):
        response = await self.client.http.delete(f"/webhooks/{self.application_id}/{self.token}/messages/@original")
        return await response.json()

    async def followup(self, message_data: dict):
        response = await self.client.http.post(f"/webhooks/{self.application_id}/{self.token}", data=message_data)
        return await response.json()

    async def fetch_followup_message(self, message_id: str):
        response = await self.client.http.get(f"/webhooks/{self.application_id}/{self.token}/messages/{message_id}")
        return await response.json()

    async def edit_followup(self, message_id: str, message_data):
        response = await self.client.http.patch(f"/webhooks/{self.application_id}/{self.token}/messages/{message_id}", data=message_data)
        return await response.json()

    async def delete_followup(self, message_id: str):
        response = await self.client.http.delete(f"/webhooks/{self.application_id}/{self.token}/messages/{message_id}")
        return await response.json()


class ModalSubmitInteraction(BaseInteraction):
    def __init__(self, client, data: dict):
        super().__init__(client, data)
        self.components: List[Union[MessageButton, MessageSelectMenu, MessageTextInput]] = []
        for component in data.get("components"):
            if component.get("type") == 2:
                self.components.append(MessageButton(component))
            elif component.get("type") == 3:
                self.components.append(MessageSelectMenu(component))
            elif component.get("type") == 4:
                self.components.append(MessageTextInput(component))

class ApplicationCommandOption:
    def __init__(self, data: dict):
        self.command_name: str = data.get("name")
        self.command_type: int = data.get("type")
        self.value: Optional[Union[str, int, float]] = data.get("value")
        self.focused: Optional[bool] = data.get("focused")

class AutoCompleteInteraction(BaseInteraction):
    def __init__(self, client, data: dict):
        super().__init__(client, data)
        self.options: List[ApplicationCommandOption] = [ApplicationCommandOption(option) for option in data.get("options", [])]

    async def reply(self, choices: List[SlashCommandOptionChoice]) -> None:
        payload = {
            "type": 9,
            "data": []
        }

        for choice in choices:
            if not isinstance(choice, SlashCommandOptionChoice):
                raise TypeError(f"{choice} must be of type SlashCommandOptionChoice")
            payload["data"]["choices"].append(choice.to_dict())

        await self.client.http.post(f"/interactions/{self.id}/{self.token}/callback", json = payload)

class MessageComponentInteraction(BaseInteraction):
    def __init__(self, client, data: dict):
        super().__init__(client, data)
        self.custom_id: str = self.data.get("custom_id")
        self.component_type: Optional[int] = self.data.get("component_type")
        self.values: Optional[dict] = [MessageSelectMenuOption(option) for option in self.data.get("values", [])]

class ApplicationCommandSubcommandOption(ApplicationCommandOption):
    def __init__(self, data: dict):
        super().__init__(data)
        self.options: List[ApplicationCommandOption] = [ApplicationCommandOption(option) for option in data.get("options", [])]

class ReceivedSlashCommandOption:
    def __init__(self, option: dict):
        self.name: str = option.get("name")
        self.value: Optional[Union[str, int, float]] = option.get("value")

class ApplicationCommandOptionResolver:
    def __init__(self, options: List[AnyOption]):

        options = []
        for option in options:
            if not option.get("options"):
                options.append(ReceivedSlashCommandOption(option))
            else:
                options.append(ApplicationCommandSubcommandOption(option))
        self.options: Optional[List[AnyOption]] = options

    def get_string_option(self, name: str) -> Optional[str]:
        filter_object = filter(lambda option: option.name == name, self.options)
        option = list(filter_object)
        if bool(option):
            return str(option[0].value)


    # def get_subcommand_option(self, name: str) -> Optional[ApplicationCommandSubcommandOption]:
    #     filter_object = filter(lambda option: option.name == name, self.options)
    #     option = list(filter_object)
    #     if bool(option):
    #         return 

    # def get_subcommand_group_option(self, name: str) -> Optional[ApplicationCommandSubcommandOption]:
    #     return list(filter(lambda option: option.name == name, self.options))[0] if len(filter(lambda option: option.name == name, self.options)) else None


    def get_int_option(self, name: str) -> Optional[int]:
        return list(filter(lambda option: option.name == name, self.options))[0].value if len(filter(lambda option: option.name == name, self.options)) else None
    
    def get_bool_option(self, name: str) -> Optional[bool]:
        return list(filter(lambda option: option.name == name, self.options))[0].value if len(filter(lambda option: option.name == name, self.options)) else None

class ResolvedDataHandler:
    def __init__(self, client, resolved_data: dict):
        self.data: dict = resolved_data # In case we miss anything and people can just do it themselves
        self.users: dict = [User(client, user) for user in self.data.get("users", [])]

        self.members: dict = [GuildMember()]
        self.roles: dict = self.data["roles"]
        self.channels: dict = self.data["channels"]

class ApplicationCommandInteraction(BaseInteraction):
    def __init__(self, client, data: dict):
        super().__init__(client, data)
        self.command_id: str = self.data.get("id")
        self.command_name: str = self.data.get("name")
        self.command_type: int = self.data.get("type")
        self.resolved: ResolvedDataHandler(client, data.get("resolved", {}))
        self.options = ApplicationCommandOptionResolver(self.data.get("options"))

class UserCommandInteraction(ApplicationCommandInteraction):
    def __init__(self, client, data: dict):
        super().__init__(client, data)
        self.target_id: str = data.get("target_id")

class MessageCommandInteraction(UserCommandInteraction):
    ... # Literally the same thing.

class MessageInteraction:
    def __init__(self, client, data: dict):
        self.id: str = data.get("id")
        self.type: int = data.get("type")
        self.name: str = data.get("name")
        self.user: User = User(client, data.get("user"))
        self.member: Optional[GuildMember] = GuildMember(client, data.get("member")) if data.get("member") else None
        self.user: User = User(client, data.get("user"))

from typing import Optional, List
from .embed import *
from .message import Message
from .user import *
class BaseInteraction:
    def __init__(self, client, data: dict):
        self.id: str = data.get("id")
        self.client = client
        self.type: int = data.get("type")
        self.application_id: int = data.get("application_id")
        self.data: dict = data
        self.interaction_data: Optional[dict] = data.get("data")
        self.guild_id: Optional[str] = data.get("guild_id")
        self.channel_id: Optional[str] = data.get("channel_id")
        self.member: Optional[GuildMember] = GuildMember(client, data.get("member")) if data.get("member") else None
        self.user: Optional[User] = User(client, data.get("user")) if data.get("user") else None
        self.token: str = data.get("token")
        self.version: int = data.get("version")
        self.locale: Optional[str] = data.get("locale")
        self.guild_locale: Optional[str] = data.get("guild_locale")
        self.original_response: Optional[Message] = None # Can't be set on construction.
        self.followup_response: Optional[Message] = None # Can't be set on construction.

    def is_application_command(self):
        return self.type == 2

    def is_message_component(self):
        return self.type == 3

    def is_autocomplete(self):
        return self.type == 4
    
    def is_modal_submit(self):
        return self.type == 5
    async def fetch_original_response(self, *, skip_cache: Optional[bool] = False):
        if not skip_cache and self.original_response:
            return self.original_response
        message_data = await self.client.http.get(f"/webhooks/{self.application_id}/{self.token}/messages/@original")
        self.original_response: Message = Message(self.client, message_data)
        return self.original_response
    
    async def edit_original_response(self, *, tts: bool = False, content: Optional[str] = None, embeds: Optional[List[Embed]] = None, allowed_mentions = None, components: Optional[List[Union[MessageButton, MessageSelectMenu, MessageTextInput]]] = None, attachments: Optional[List[Attachment]] = None, suppress_embeds: Optional[bool] = False, ephemeral: Optional[bool] = False) -> None:

        message_data = {
            "tts": tts,
            "flags": 0
        }

        if suppress_embeds:
            message_data["flags"] += 1 << 2
        if ephemeral:
            message_data["flags"] += 1 << 6

        if content:
            message_data["content"] = content
        if embeds:
            message_data["embeds"] = [embed.to_dict() for embed in embeds]
        if allowed_mentions:
            message_data["allowed_mentions"] = allowed_mentions.to_dict()
        if components:
            message_data["components"] = [component.to_dict() for component in components]
        if attachments:
            message_data["attachments"] = [attachment.to_dict() for attachment in attachments]

        new_message_data = await self.client.http.patch(f"/webhooks/{self.application_id}/{self.token}/messages/@original", json = message_data)
        self.original_response: Message = Message(self.client, new_message_data)
        return self.original_response
    
    async def delete_original_response(self):
        await self.client.http.delete(f"/webhooks/{self.application_id}/{self.token}/messages/@original")

    async def create_followup(self, *, tts: bool = False, content: Optional[str] = None, embeds: Optional[List[Embed]] = None, allowed_mentions = None, components: Optional[List[Union[MessageButton, MessageSelectMenu, MessageTextInput]]] = None, attachments: Optional[List[Attachment]] = None, suppress_embeds: Optional[bool] = False, ephemeral: Optional[bool] = False) -> None:

        message_data = {
            "tts": tts,
            "flags": 0
        }

        if suppress_embeds:
            message_data["flags"] += 1 << 2
        if ephemeral:
            message_data["flags"] += 1 << 6

        if content:
            message_data["content"] = content
        if embeds:
            message_data["embeds"] = [embed.to_dict() for embed in embeds]
        if allowed_mentions:
            message_data["allowed_mentions"] = allowed_mentions.to_dict()
        if components:
            message_data["components"] = [component.to_dict() for component in components]
        if attachments:
            message_data["attachments"] = [attachment.to_dict() for attachment in attachments]

        new_message_data = await self.client.http.post(f"/webhooks/{self.application_id}/{self.token}/", json = message_data)
        self.followup_response: Message = Message(self.client, new_message_data)
        return self.followup_response

    async def edit_followup(self, *, tts: bool = False, content: Optional[str] = None, embeds: Optional[List[Embed]] = None, allowed_mentions = None, components: Optional[List[Union[MessageButton, MessageSelectMenu, MessageTextInput]]] = None, attachments: Optional[List[Attachment]] = None, suppress_embeds: Optional[bool] = False, ephemeral: Optional[bool] = False) -> None:

        message_data = {
            "tts": tts,
            "flags": 0
        }

        if suppress_embeds:
            message_data["flags"] += 1 << 2
        if ephemeral:
            message_data["flags"] += 1 << 6

        if content:
            message_data["content"] = content
        if embeds:
            message_data["embeds"] = [embed.to_dict() for embed in embeds]
        if allowed_mentions:
            message_data["allowed_mentions"] = allowed_mentions.to_dict()
        if components:
            message_data["components"] = [component.to_dict() for component in components]
        if attachments:
            message_data["attachments"] = [attachment.to_dict() for attachment in attachments]

        await self.client.http.patch(f"/webhook/{self.application_id}/{self.token}/", json = message_data)

    async def delete_followup(self):
        return await self.client.http.delete(f"/webhook/{self.application_id}/{self.token}/")

class MessageComponentInteraction(BaseInteraction):
    def __init__(self, client, data: dict):
        super().__init__(client, data)
        self.custom_id: str = self.data.get("custom_id")
        self.component_type: Optional[int] = self.data.get("component_type")
        self.values: Optional[dict] = [MessageSelectMenuOption(option) for option in self.data.get("values", [])]

    async def update(self, *, tts: bool = False, content: Optional[str] = None, embeds: Optional[List[Embed]] = None, allowed_mentions = None, components: Optional[List[Union[MessageButton, MessageSelectMenu, MessageTextInput]]] = None, attachments: Optional[List[Attachment]] = None, suppress_embeds: Optional[bool] = False, ephemeral: Optional[bool] = False) -> None:

        message_data = {
            "tts": tts,
            "flags": 0
        }

        if suppress_embeds:
            message_data["flags"] += 1 << 2
        if ephemeral:
            message_data["flags"] += 1 << 6

        if content:
            message_data["content"] = content
        if embeds:
            message_data["embeds"] = [embed.to_dict() for embed in embeds]
        if allowed_mentions:
            message_data["allowed_mentions"] = allowed_mentions.to_dict()
        if components:
            message_data["components"] = [component.to_dict() for component in components]
        if attachments:
            message_data["attachments"] = [attachment.to_dict() for attachment in attachments]

        payload = {
            "type": 7,
            "data": message_data
        }

        await self.client.http.patch(f"/interaction/{self.id}/{self.token}/callback", json = payload)

    async def defer_update(self):
        await self.client.http.post(f"/interaction/{self.id}/{self.token}/callback", json = {
            "type": 6
        })


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



class ResolvedDataHandler:
    def __init__(self, client, resolved_data: dict):
        self.data: dict = resolved_data # In case we miss anything and people can just do it themselves
        self.users: dict = [User(client, user) for user in self.data.get("users", [])]

        self.members: dict = [GuildMember()]
        self.roles: dict = self.data["roles"]
        self.channels: dict = self.data["channels"]


    
    
class UserCommandInteraction(ApplicationCommandInteraction):
    def __init__(self, client, data: dict):
        super().__init__(client, data)
        self.target_id: str = data.get("target_id")

class MessageCommandInteraction(UserCommandInteraction):
    ... # Literally the same thing.
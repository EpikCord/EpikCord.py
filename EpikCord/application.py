from typing import (Optional, Union, List,)
from .__init__ import PartialUser, Team, BaseInteraction, ResolvedDataHandler, Modal,InvalidArgumentType,Embed,MessageButton,MessageSelectMenu,MessageTextInput,Attachment
#temp import (So many!)
# we have to make sure there is no circular imports, someone help us!
class Application:
    def __init__(self, data: dict):
        self.id: str = data.get("id")
        self.name: str = data.get("name")
        self.icon: Optional[str] = data.get("icon")
        self.description: str = data.get("description")
        self.rpc_origins: Optional[list] = data.get("rpc_origins")
        self.bot_public: bool = data.get("bot_public")
        self.bot_require_code_grant: bool = data.get("bot_require_code_grant")
        self.terms_of_service_url: Optional[str] = data.get("terms_of_service")
        self.privacy_policy_url: Optional[str] = data.get("privacy_policy")
        self.owner: Optional[PartialUser] = PartialUser(data.get("user")) if data.get("user") else None
        self.summary: str = data.get("summary")
        self.verify_key: str = data.get("verify_key")
        self.team: Optional[Team] = Team(data.get("team")) if data.get("get") else None
        self.cover_image: Optional[str] = data.get("cover_image")
        self.flags: int = data.get("flags")

class ApplicationCommand:
    def __init__(self, data: dict):
        self.id: str = data.get("id")
        self.type: int = data.get("type")
        self.application_id: str = data.get("application_id")
        self.guild_id: Optional[str] = data.get("guild_id")
        self.name: str = data.get("name")
        self.description: str = data.get("description")
        self.default_permissions: bool = data.get("default_permissions")
        self.version: str = data.get("version")

class ApplicationCommandPermission:
    def __init__(self, data: dict):
        self.id: str = data.get("id")
        self.type: int = data.get("type")
        self.permission: bool = data.get("permission")

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "permission": self.permission
        }

class ApplicationCommandOption:
    def __init__(self, data: dict):
        self.command_name: str = data.get("name")
        self.command_type: int = data.get("type")
        self.value: Optional[Union[str, int, float]] = data.get("value")
        self.focused: Optional[bool] = data.get("focused")

class ApplicationCommandSubcommandOption(ApplicationCommandOption):
    def __init__(self, data: dict):
        super().__init__(data)
        self.options: List[ApplicationCommandOption] = [ApplicationCommandOption(option) for option in data.get("options", [])]

class ApplicationCommandInteraction(BaseInteraction):
    def __init__(self, client, data: dict):
        super().__init__(client, data)
        self.command_id: str = self.interaction_data.get("id")
        self.command_name: str = self.interaction_data.get("name")
        self.command_type: int = self.interaction_data.get("type")
        self.resolved: ResolvedDataHandler(client, data.get("resolved", {}))
        self.options: List[dict] | None = self.interaction_data.get("options", [])

    
    async def send_modal(self, modal: Modal):
        if not isinstance(modal, Modal):
            raise InvalidArgumentType("The modal argument must be of type Modal.")
        payload = {
            "type": 9,
            "data": modal.to_dict()
        }
        await self.client.http.post(f"/interactions/{self.id}/{self.token}/callback", json=payload)

    async def reply(self, *, tts: bool = False, content: Optional[str] = None, embeds: Optional[List[Embed]] = None, allowed_mentions = None, components: Optional[List[Union[MessageButton, MessageSelectMenu, MessageTextInput]]] = None, attachments: Optional[List[Attachment]] = None, suppress_embeds: Optional[bool] = False, ephemeral: Optional[bool] = False) -> None:

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
            "type": 4,
            "data": message_data
        }
        await self.client.http.post(f"/interactions/{self.id}/{self.token}/callback", json = payload)
    
    async def defer(self, *, show_loading_state: Optional[bool] = True):
        if show_loading_state:
            return await self.client.http.post(f"/interaction/{self.id}/{self.token}/callback", json = {"type": 5})
        else:
            return await self.client.http.post(f"/interaction/{self.id}/{self.token}/callback", json = {"type": 6})
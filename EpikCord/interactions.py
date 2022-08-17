from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, Union

from .abstract import BaseInteraction
from .components import *
from .options import *

if TYPE_CHECKING:
    from .message import Attachment, Embed


class Modal:
    def __init__(self, *, title: str, custom_id: str, components: List[ActionRow]):
        self.title = title
        self.custom_id = custom_id
        self.components = [component.to_dict() for component in components]

    def to_dict(self):
        return {
            "title": self.title,
            "custom_id": self.custom_id,
            "components": [component.to_dict() for component in self.components],
        }


class ResolvedDataHandler:
    def __init__(self, client, resolved_data: dict):
        self.data: dict = resolved_data
        ...


class MessageComponentInteraction(BaseInteraction):
    def __init__(self, client, data: dict):
        from EpikCord import Message

        super().__init__(client, data)
        self.message: Message = Message(client, data.get("message"))
        self.custom_id: str = self.interaction_data.get("custom_id")
        self.component_type: Optional[int] = self.interaction_data.get("component_type")
        self.values: Optional[dict] = [
            SelectMenuOption(option)
            for option in self.interaction_data.get("values", [])
        ]

    def is_action_row(self):
        return self.component_type == 1

    def is_button(self):
        return self.component_type == 2

    def is_select_menu(self):
        return self.component_type == 3

    def is_text_input(self):
        return self.component_type == 4

    async def update(
        self,
        *,
        tts: bool = False,
        content: Optional[str] = None,
        embeds: Optional[List[Embed]] = None,
        allowed_mentions=None,
        components: Optional[List[Union[Button, SelectMenu, TextInput]]] = None,
        attachments: Optional[List[Attachment]] = None,
        suppress_embeds: Optional[bool] = False,
    ) -> None:

        message_data = {"tts": tts, "flags": 0}

        if suppress_embeds:
            message_data["flags"] += 1 << 2

        if content:
            message_data["content"] = content
        if embeds:
            message_data["embeds"] = [embed.to_dict() for embed in embeds]
        if allowed_mentions:
            message_data["allowed_mentions"] = allowed_mentions.to_dict()
        if components:
            message_data["components"] = [
                component.to_dict() for component in components
            ]
        if attachments:
            message_data["attachments"] = [
                attachment.to_dict() for attachment in attachments
            ]

        payload = {"type": 7, "data": message_data}

        await self.client.http.patch(
            f"/interaction/{self.id}/{self.token}/callback", json=payload
        )

    async def defer_update(self):
        await self.client.http.post(
            f"/interaction/{self.id}/{self.token}/callback", json={"type": 6}
        )


class ModalSubmitInteraction(BaseInteraction):
    def __init__(self, client, data: dict):
        super().__init__(client, data)
        self.custom_id: str = self.interaction_data["custom_id"]
        self._components: List[
            Union[Button, SelectMenu, TextInput]
        ] = self.interaction_data.get("components")

    async def send_modal(self, *_, **__):
        raise NotImplementedError("ModalSubmitInteractions cannot send modals.")


class AutoCompleteInteraction(BaseInteraction):
    def __init__(self, client, data: dict):
        super().__init__(client, data)
        conversion_type = {
            1: Subcommand,
            2: SubCommandGroup,
            3: StringOption,
            4: IntegerOption,
            5: BooleanOption,
            6: UserOption,
            7: ChannelOption,
            8: RoleOption,
            9: MentionableOption,
            10: NumberOption,
            11: AttachmentOption,
        }
        self.options: List[AnyOption] = [
            conversion_type[option["type"]] for option in data.get("options", [])
        ]

    async def reply(self, choices: List[SlashCommandOptionChoice]) -> None:
        payload = {"type": 9, "data": []}

        for choice in choices:
            if not isinstance(choice, SlashCommandOptionChoice):
                raise TypeError(f"{choice} must be of type SlashCommandOptionChoice")
            payload["data"]["choices"].append(choice.to_dict())

        await self.client.http.post(
            f"/interactions/{self.id}/{self.token}/callback", json=payload
        )


class ApplicationCommandInteraction(BaseInteraction):
    def __init__(self, client, data: dict):
        super().__init__(client, data)
        self.command_id: str = self.interaction_data.get("id")
        self.command_name: str = self.interaction_data.get("name")
        self.command_type: int = self.interaction_data.get("type")
        self.resolved = ResolvedDataHandler(client, data.get("resolved", {}))
        self.options: List[dict] | None = self.interaction_data.get("options", [])


class UserCommandInteraction(ApplicationCommandInteraction):
    def __init__(self, client, data: dict):
        super().__init__(client, data)
        self.target_id: str = data.get("target_id")


class MessageCommandInteraction(UserCommandInteraction):
    ...  # Literally the same thing.


class MessageInteraction:
    def __init__(self, client, data: dict):
        from EpikCord import GuildMember, User

        self.id: str = data.get("id")
        self.type: int = data.get("type")
        self.name: str = data.get("name")
        self.user: User = User(client, data.get("user"))
        payload = {}
        if data.get("user"):
            payload.update(data.get("user"))
        if data.get("member"):
            payload.update(data.get("member"))
        if data.get("user") and not data.get("member"):
            payload = {**data.get("user")}

        self.member: Optional[GuildMember] = (
            GuildMember(client, payload) if data.get("member") else None
        )
        self.user = User(client, data.get("user"))


__all__ = (
    "Modal",
    "ModalSubmitInteraction",
    "ResolvedDataHandler",
    "MessageComponentInteraction",
    "AutoCompleteInteraction",
    "ApplicationCommandInteraction",
    "UserCommandInteraction",
    "MessageCommandInteraction",
    "MessageInteraction",
)

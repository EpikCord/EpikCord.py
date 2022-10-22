from __future__ import annotations

from typing import TYPE_CHECKING, List, Literal, Optional, TypedDict, Union
from typing_extensions import NotRequired

from .abstract import BaseInteraction
from .components import *
from .options import *

if TYPE_CHECKING:
    import discord_typings

    from .message import Attachment, Embed, MessagePayload


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
    def __init__(
        self, client, resolved_data: discord_typings.ResolvedInteractionDataData
    ):
        self.data: discord_typings.ResolvedInteractionDataData = resolved_data

class DeferredInteractionResponse(TypedDict):
    type: Literal[5, 6]
    data: NotRequired[Optional[MessagePayload]]

class BaseComponentInteraction(BaseInteraction):
    def __init__(self, client, data: discord_typings.ComponentInteractionData):
        super().__init__(client, data)
        from EpikCord import Message

        self.message: Message = Message(client, data["message"])
        self.custom_id: str = data["data"]["custom_id"]
        self.component_type: int = data["data"]["component_type"]

    async def defer(self, *, ephemeral: bool = False, show_loading_state: bool = True):
        data: DeferredInteractionResponse = {"type": 5}

        if ephemeral: data["data"] = {"flags": 1 << 6}

        if not show_loading_state:
            data["type"] = 6

        await self.client.http.post(
            f"/interaction/{self.id}/{self.token}/callback", json=data
        )

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

        message_data: MessagePayload = {"tts": tts, "flags": 0}

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


class ButtonInteraction(BaseComponentInteraction):
    ...


class SelectMenuInteraction(BaseComponentInteraction):
    def __init__(self, client, data):
        super().__init__(client, data)
        self.values: List[discord_typings.SelectMenuOptionData] = data["data"]["values"]


class ModalSubmitInteraction(BaseInteraction):
    def __init__(self, client, data: dict):
        super().__init__(client, data)
        self.custom_id: str = data["data"]["custom_id"]
        self._components: List[Union[Button, SelectMenu, TextInput]] = data["data"][
            "components"
        ]

    async def send_modal(self, *_, **__):
        raise NotImplementedError("ModalSubmitInteractions cannot send modals.")


class AutoCompleteInteractionData(TypedDict):
    choices: List[
        Union[
            discord_typings.interactions.commands.StrCommandOptionChoiceData,
            discord_typings.interactions.commands.IntCommandOptionChoiceData,
        ]
    ]


class AutoCompleteInteractionResponse(TypedDict):
    type: Literal[9]
    data: AutoCompleteInteractionData


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
            conversion_type[option["type"]](**option)
            for option in data.get("options", [])
        ]

    async def reply(self, choices: List[SlashCommandOptionChoice]) -> None:  # type: ignore
        payload: AutoCompleteInteractionResponse = {"type": 9, "data": {"choices": []}}

        for choice in choices:
            if not isinstance(choice, SlashCommandOptionChoice):
                raise TypeError(f"{choice} must be of type SlashCommandOptionChoice")

            payload["data"]["choices"].append(choice.to_dict())

        await self.client.http.post(
            f"/interactions/{self.id}/{self.token}/callback", json=payload
        )


class ApplicationCommandInteraction(BaseInteraction):
    def __init__(self, client, data: discord_typings.ApplicationCommandInteractionData):
        super().__init__(client, data)
        self.command_id: int = int(data["data"]["id"])
        self.command_name: str = data["data"]["name"]
        self.command_type: int = data["data"]["type"]
        self.resolved = (
            ResolvedDataHandler(client, data["data"]["resolved"])
            if data.get("resolved")
            else None
        )
        self.options: Optional[List[ReceivedOption]] = (
            [ReceivedOption(option) for option in data["data"]["options"]]
            if data["data"].get("options")
            else None
        )


class UserCommandInteraction(ApplicationCommandInteraction):
    def __init__(self, client, data):
        super().__init__(client, data)
        self.target_id: str = data.get("target_id")


class MessageCommandInteraction(UserCommandInteraction):
    ...  # Literally the same thing.


class MessageInteraction:
    def __init__(self, client, data: discord_typings.MessageInteractionData):
        from EpikCord import GuildMember, User

        self.id: int = int(data["id"])
        self.type: int = data["type"]
        self.name: str = data["name"]
        self.user: User = User(client, data["user"])
        self.member: Optional[GuildMember] = GuildMember(client, {**data["member"], **data["user"]}) if data.get("member") else None  # type: ignore


AnyInteraction = Union[
    ButtonInteraction,
    SelectMenuInteraction,
    ModalSubmitInteraction,
    AutoCompleteInteraction,
    ApplicationCommandInteraction,
    UserCommandInteraction,
    MessageCommandInteraction,
]

__all__ = (
    "Modal",
    "ModalSubmitInteraction",
    "ResolvedDataHandler",
    "ButtonInteraction",
    "SelectMenuInteraction",
    "AutoCompleteInteraction",
    "ApplicationCommandInteraction",
    "UserCommandInteraction",
    "MessageCommandInteraction",
    "MessageInteraction",
)

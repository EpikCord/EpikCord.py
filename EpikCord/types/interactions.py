from typing import Dict, List, Literal, TypedDict, Union

from discord_typings import (
    ActionRowData,
    ApplicationCommandOptionInteractionData,
    GuildMemberData,
    MessageData,
    ResolvedInteractionDataData,
    UserData,
)
from typing_extensions import NotRequired


class BaseInteractionData(TypedDict):
    id: str
    application_id: str
    type: Literal[1, 2, 3, 4, 5]
    guild_id: NotRequired[str]
    channel_id: NotRequired[str]
    member: NotRequired[GuildMemberData]
    user: NotRequired[UserData]
    token: str
    version: int
    message: NotRequired[MessageData]
    app_permissions: NotRequired[str]
    locale: NotRequired[str]
    guild_locale: NotRequired[str]


class BaseApplicationCommandDataData(TypedDict):
    id: str
    name: str
    resolved: NotRequired[ResolvedInteractionDataData]
    guild_id: NotRequired[str]


class ChatInputInteractionDataData(BaseApplicationCommandDataData):
    type: Literal[1]
    options: List[ApplicationCommandOptionInteractionData]


class BaseContextMenuInteractionDataData(BaseApplicationCommandDataData):
    target_id: str


class MessageContextMenuInteractionDataData(BaseContextMenuInteractionDataData):
    type: Literal[2]


class UserContextMenuInteractionDataData(BaseContextMenuInteractionDataData):
    type: Literal[3]


class ButtonInteractionDataData(TypedDict):
    custom_id: str
    component_type: Literal[2, 3, 5, 6, 7, 8]


class SelectMenuInteractionDataData(ButtonInteractionDataData):
    values: List[str]


class ModalSubmitInteractionDataData(TypedDict):
    custom_id: str
    components: List[ActionRowData]


class ChatInputInteractionData(BaseInteractionData):
    data: ChatInputInteractionDataData


class MessageContextMenuInteractionData(BaseInteractionData):
    data: MessageContextMenuInteractionDataData


class UserContextMenuInteractionData(BaseInteractionData):
    data: UserContextMenuInteractionDataData


class ButtonInteractionData(BaseInteractionData):
    data: ButtonInteractionDataData


class SelectMenuInteractionData(BaseInteractionData):
    data: SelectMenuInteractionDataData


class ModalSubmitInteractionData(BaseInteractionData):
    data: ModalSubmitInteractionDataData


InteractionDataData = Union[
    ButtonInteractionDataData,
    SelectMenuInteractionDataData,
    ChatInputInteractionDataData,
    ModalSubmitInteractionDataData,
]

InteractionData = Union[
    ButtonInteractionData,
    SelectMenuInteractionData,
    ChatInputInteractionData,
    ModalSubmitInteractionData,
    MessageContextMenuInteractionData,
    UserContextMenuInteractionData,
]


class ApplicationCommandChoiceData(TypedDict):
    name: str
    value: Union[str, int, float]
    name_localizations: NotRequired[Dict[str, str]]

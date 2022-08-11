from enum import IntEnum
from typing import Union, Optional, List

from .exceptions import (
    InvalidArgumentType,
    CustomIdIsTooBig,
    InvalidComponentStyle,
    TooManySelectMenuOptions,
    TooManyComponents,
    LabelIsTooBig,
)
from .partials import PartialEmoji


class SelectMenuOption:
    def __init__(
        self,
        label: str,
        value: str,
        description: Optional[str] = None,
        emoji: Optional[PartialEmoji] = None,
        default: Optional[bool] = None,
    ):
        self.label: str = label
        self.value: str = value
        self.description: Optional[str] = description
        self.emoji: Optional[PartialEmoji] = emoji
        self.default: Optional[bool] = default

    def to_dict(self):
        settings = {"label": self.label, "value": self.value}

        if self.description:
            settings["description"] = self.description

        if self.emoji:
            if isinstance(self.emoji, PartialEmoji):
                settings["emoji"] = self.emoji.to_dict()

            elif isinstance(self.emoji, dict):
                settings["emoji"] = self.emoji

        if self.default:
            settings["default"] = self.default

        return settings


class BaseComponent:
    def __init__(self, *, custom_id: str):
        self.custom_id: str = custom_id

    def set_custom_id(self, custom_id: str):

        if not isinstance(custom_id, str):
            raise InvalidArgumentType("Custom Id must be a string.")

        elif len(custom_id) > 100:
            raise CustomIdIsTooBig("Custom Id must be 100 characters or less.")

        self.custom_id = custom_id


class SelectMenu(BaseComponent):
    def __init__(
        self,
        *,
        min_values: Optional[int] = 1,
        max_values: Optional[int] = 1,
        disabled: Optional[bool] = False,
        custom_id: str
    ):
        super().__init__(custom_id=custom_id)
        self.options: List[Union[SelectMenuOption, dict]] = []
        self.type: str = 3
        self.min_values = min_values
        self.max_values = max_values
        self.disabled: bool = disabled

    def to_dict(self):
        return {
            "type": self.type,
            "options": self.options,
            "min_values": self.min_values,
            "max_values": self.max_values,
            "disabled": self.disabled,
            "custom_id": self.custom_id,
        }

    def add_options(self, options: List[SelectMenuOption]):
        for option in options:

            if len(self.options) > 25:
                raise TooManySelectMenuOptions(
                    "You can only have 25 options in a select menu."
                )

            self.options.append(option.to_dict())
        return self

    def set_placeholder(self, placeholder: str):
        if not isinstance(placeholder, str):
            raise InvalidArgumentType("Placeholder must be a string.")

        self.settings["placeholder"] = placeholder
        return self

    def set_min_values(self, min: int):
        if not isinstance(min, int):
            raise InvalidArgumentType("Min must be an integer.")

        self.options["min_values"] = min
        return self

    def set_max_values(self, max: int):
        if not isinstance(max, int):
            raise InvalidArgumentType("Max must be an integer.")

        self.options["max_values"] = max
        return self

    def set_disabled(self, disabled: bool):
        self.disabled = disabled


class TextInput(BaseComponent):
    def __init__(
        self,
        *,
        custom_id: str,
        style: Union[int, str] = 1,
        label: str,
        min_length: Optional[int] = 1,
        max_length: Optional[int] = 4000,
        required: Optional[bool] = True,
        value: Optional[str] = None,
        placeholder: Optional[str] = None
    ):
        super().__init__(custom_id=custom_id)
        VALID_STYLES = {"Short": 1, "Paragraph": 2}

        if isinstance(style, str):
            if style not in VALID_STYLES:
                raise InvalidComponentStyle(
                    "Style must be either 'Short' or 'Paragraph'."
                )
            style = VALID_STYLES[style]

        elif isinstance(style, int):
            if style not in VALID_STYLES.values():
                raise InvalidComponentStyle("Style must be either 1 or 2.")

        self.style: int = style
        self.type: int = 4
        self.label: str = label
        self.min_length: int = min_length
        self.max_length: int = max_length
        self.required: bool = required
        self.value: Optional[str] = value
        self.placeholder: Optional[str] = placeholder

    def to_dict(self):
        payload = {
            "type": 4,
            "custom_id": self.custom_id,
            "style": self.style,
            "label": self.label,
            "required": self.required,
        }

        if self.min_length:
            payload["min_length"] = self.min_length

        if self.max_length:
            payload["max_length"] = self.max_length

        if self.value:
            payload["value"] = self.value

        if self.placeholder:
            payload["placeholder"] = self.placeholder

        return payload


class ButtonStyle(IntEnum):
    PRIMARY = 1
    SECONDARY = 2
    SUCCESS = GREEN = 3
    DANGER = RED = 4
    LINK = 5


class Button(BaseComponent):
    def __init__(
        self,
        *,
        style: Optional[Union[int, str]] = None,
        label: Optional[str] = None,
        emoji: Optional[Union[PartialEmoji, dict]] = None,
        url: Optional[str] = None,
        custom_id: str,
        disabled: bool = False
    ):
        super().__init__(custom_id=custom_id)
        self.type: int = 2
        self.disabled = disabled
        self.style: Optional[Union[int, str]] = style or 1

        if url or style == ButtonStyle.LINK:
            self.url: Optional[str] = url
            self.style = 5
        else:
            self.url = None

        self.emoji: Optional[Union[PartialEmoji, dict]] = emoji
        self.label: Optional[str] = label

    def set_style(self, style: Union[ButtonStyle, str]):
        # check from ButtonStyle IntEnum
        if isinstance(style, str):
            if not ButtonStyle[style]:
                raise InvalidArgumentType("Style must be in ButtonStyle enum.")

            style = ButtonStyle[style]
            return self

        elif isinstance(style, ButtonStyle):
            style = style.value
            return self

        elif style in [1, 2, 3, 4, 5]:
            self.style = style

        raise InvalidComponentStyle(
            "Invalid button style. Style must be one of the following: "
            + ", ".join(btn_style.name for btn_style in ButtonStyle)
        )

    def to_dict(self):
        from EpikCord import Utils

        settings = Utils.filter_values(
            {
                "type": self.type,
                "custom_id": self.custom_id,
                "disabled": self.disabled,
                "style": self.style,
                "label": self.label,
                "url": self.url,
                "emoji": self.emoji,
            }
        )

        return settings

    def set_label(self, label: str):
        if not isinstance(label, str):
            raise InvalidArgumentType("Label must be a string.")

        if len(label) > 80:
            raise LabelIsTooBig("Label must be 80 characters or less.")

        self.label = label
        return self

    def set_emoji(self, emoji: Union[PartialEmoji, dict]):
        if isinstance(emoji, dict):
            self.emoji = emoji
            return self

        elif isinstance(emoji, PartialEmoji):
            self.emoji = emoji.data
            return self
        raise InvalidArgumentType(
            "Emoji must be a PartialEmoji or a dict that represents a PartialEmoji."
        )

    def set_url(self, url: str):

        if not isinstance(url, str):
            raise InvalidArgumentType("Url must be a string.")

        self.url = url
        self.style = 5
        return self

    @classmethod
    def from_dict(self, data):
        return Button(
            **{
                "custom_id": data["custom_id"],
                "style": data.get("style"),
                "label": data.get("label"),
                "emoji": data.get("emoji"),
                "url": data.get("url"),
                "disabled": data.get("disabled"),
            }
        )


def component_from_type(component_data: dict):
    component_type = component_data["type"]
    del component_data["type"]
    if component_type == 2:
        return Button(**component_data)
    elif component_type == 3:
        return SelectMenu(**component_data)
    elif component_type == 4:
        return TextInput(**component_data)


class ActionRow:
    def __init__(
        self, components: Optional[List[Union[Button, SelectMenu, TextInput]]] = None
    ):
        self.type: int = 1
        self.components: List[Union[TextInput, Button, SelectMenu]] = components or []

    def to_dict(self):
        return {
            "type": self.type,
            "components": [component.to_dict() for component in self.components],
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            [component_from_type(component) for component in data.get("components")]
        )

    @staticmethod
    def check_still_valid(list_of_components):
        buttons = 0
        select_menus = 0
        text_inputs = 0

        for component in list_of_components:

            if isinstance(component, Button):
                buttons += 1

            elif isinstance(component, SelectMenu):
                select_menus += 1

            elif isinstance(component, TextInput):
                text_inputs += 1

            if buttons >= 5 and text_inputs < 1 and select_menus < 1:
                raise TooManyComponents(
                    "You can only have 1 SelectMenu/TextInput per ActionRow"
                    " or 5 Buttons per ActionRow."
                )

            yield component

    def add_components(self, components: List[Union[Button, SelectMenu]]):
        for component in self.check_still_valid(components):
            self.components.append(component.to_dict())

    def add_component(self, component: Union[Button, SelectMenu, TextInput]):
        for component in self.check_still_valid(self.components):
            ...  # Just let the validator run

        self.components.append(component.to_dict())

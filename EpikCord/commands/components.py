from ..emoji import PartialEmoji
from ..errors import (
    InvalidArgumentType, 
    CustomIdIsTooBig, 
    TooManyComponents, 
    TooManySelectMenuOptions, 
    InvalidComponentStyle,
    MissingCustomId, 
    LabelIsTooBig
)
from typing import Optional, List, Union

class BaseComponent:
    def __init__(self, *, custom_id: str):
        self.custom_id: str = custom_id

    def set_custom_id(self, custom_id: str):

        if not isinstance(custom_id, str):
            raise InvalidArgumentType("Custom Id must be a string.")

        elif len(custom_id) > 100:
            raise CustomIdIsTooBig("Custom Id must be 100 characters or less.")

        self.settings["custom_id"] = custom_id

class MessageSelectMenuOption:
    def __init__(self, label: str, value: str, description: Optional[str] = None, emoji: Optional[PartialEmoji] = None, default: Optional[bool] = None):
        self.label: str = label
        self.value: str = value
        self.description: Optional[str] = description
        self.emoji: Optional[PartialEmoji] = emoji
        self.default: Optional[bool] = default

    def to_dict(self):
        settings = {
            "label": self.label,
            "value": self.value
        }

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


class MessageSelectMenu(BaseComponent):
    def __init__(self, *, min_values: Optional[int] = 1, max_values: Optional[int] = 1, disabled: Optional[bool] = False, custom_id: str):
        super().__init__(custom_id=custom_id)
        self.options: List[Union[MessageSelectMenuOption, dict]] = []
        self.type: str = 3
        self.min_values = min_values
        self.max_values = max_values
        self.disabled: bool = disabled

    def to_dict(self):
        settings = {
            "type": self.type,
            "options": self.options,
            "min_values": self.min_values,
            "max_values": self.max_values,
            "disabled": self.disabled,
            "custom_id": self.custom_id
        }
        return settings

    def add_options(self, options: List[MessageSelectMenuOption]):
        for option in options:

            if len(self.options) > 25:
                raise TooManySelectMenuOptions(
                    "You can only have 25 options in a select menu.")

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


class MessageTextInput(BaseComponent):
    def __init__(self, *, custom_id: str, style: Union[int, str] = 1, label: str, min_length: Optional[int] = 10, max_length: Optional[int] = 4000, required: Optional[bool] = True, value: Optional[str] = None, placeholder: Optional[str] = None):
        super().__init__(custom_id=custom_id)
        VALID_STYLES = {
            "Short": 1,
            "Paragraph": 2
        }

        if isinstance(style, str):
            if style not in VALID_STYLES:
                raise InvalidComponentStyle(
                    "Style must be either 'Short' or 'Paragraph'.")
            style = VALID_STYLES[style]

        elif isinstance(style, int):
            if style not in VALID_STYLES.values():
                raise InvalidComponentStyle("Style must be either 1 or 2.")

        self.style: int = style
        self.label: str = label
        self.min_length: int = min_length
        self.max_length: int = max_length
        self.required: bool = required
        self.value: str = value
        self.placeholder: Optional[str] = placeholder

    def to_dict(self):
        settings: dict = {
            "type": self.type,
            "label": self.label,
            "min_length": self.min_length,
            "max_length": self.max_length,
            "required": self.required,
            "style": self.style,
        }

        if getattr(self, "value", None):
            settings["value"] = self.value

        if getattr(self, "placeholder", None):
            settings["placeholder"] = self.placeholder


class MessageButton(BaseComponent):
    def __init__(self, *, style: Optional[Union[int, str]] = 1, label: Optional[str] = None, emoji: Optional[Union[PartialEmoji, dict]] = None, url: Optional[str] = None, custom_id: str, disabled: bool = False):
        super().__init__(custom_id=custom_id)
        self.type: int = 2
        self.disabled = disabled
        valid_styles = {
            "PRIMARY": 1,
            "SECONDARY": 2,
            "SUCCESS": 3,
            "DANGER": 4,
            "LINK": 5
        }

        if isinstance(style, str):
            if style.upper() not in valid_styles:
                raise InvalidComponentStyle(
                    "Invalid button style. Style must be one of PRIMARY, SECONDARY, LINK, DANGER, or SUCCESS.")
            self.style: int = valid_styles[style.upper()]

        elif isinstance(style, int):
            if style not in valid_styles.values():
                raise InvalidComponentStyle(
                    "Invalid button style. Style must be in range 1 to 5 inclusive.")
            self.style: int = style

        if url:
            self.url: Optional[str] = url
            self.style: int = 5
        if emoji:
            self.emoji: Optional[Union[PartialEmoji, dict]] = emoji
        if label:
            self.label: Optional[str] = label

    @property
    def PRIMARY(self):
        self.style = 1
        return self
    
    @property
    def SECONDARY(self):
        self.style = 2
        return self
    
    @property
    def SUCCESS(self):
        self.style = 3
        return self
    GREEN = SUCCESS
    @property
    def DANGER(self):
        self.style = 4
        return self
    RED = DANGER
    @property
    def LINK(self):
        self.style = 5
        return self 

    def to_dict(self):
        settings = {
            "type": self.type,
            "custom_id": self.custom_id,
            "disabled": self.disabled,
            "style": self.style,
        }

        if getattr(self, "label", None):
            settings["label"] = self.label

        if getattr(self, "url", None):
            settings["url"] = self.url

        if getattr(self, "emoji", None):
            settings["emoji"] = self.emoji

        return settings

    def set_label(self, label: str):

        if not isinstance(label, str):
            raise InvalidArgumentType("Label must be a string.")

        if len(label) > 80:
            raise LabelIsTooBig("Label must be 80 characters or less.")

        self.settings["label"] = label
        return self

    def set_style(self, style: Union[int, str]):
        valid_styles = {
            "PRIMARY": 1,
            "SECONDARY": 2,
            "SUCCESS": 3,
            "DANGER": 4,
            "LINK": 5
        }
        if isinstance(style, str):
            if style.upper() not in valid_styles:
                raise InvalidComponentStyle(
                    "Invalid button style. Style must be one of PRIMARY, SECONDARY, LINK, DANGER, or SUCCESS.")
            self.settings["style"] = valid_styles[style.upper()]
            return self

        elif isinstance(style, int):
            if style not in valid_styles.values():
                raise InvalidComponentStyle(
                    "Invalid button style. Style must be in range 1 to 5 inclusive.")
            self.settings["style"] = style
            return self

    def set_emoji(self, emoji: Union[PartialEmoji, dict]):

        if isinstance(emoji, dict):
            self.settings["emoji"] = emoji
            return self

        elif isinstance(emoji, PartialEmoji):
            self.settings["emoji"] = emoji.data
            return self
        raise InvalidArgumentType(
            "Emoji must be a PartialEmoji or a dict that represents a PartialEmoji.")

    def set_url(self, url: str):

        if not isinstance(url, str):
            raise InvalidArgumentType("Url must be a string.")

        self.settings["url"] = url
        self.settings["style"] = 5
        return self


class MessageActionRow:
    def __init__(self, components: Optional[List[Union[MessageButton, MessageSelectMenu]]] = None):
        self.settings = {
            "type": 1,
            "components": components or []
        }
        self.type: int = 1
        self.components: List[Union[MessageTextInput, MessageButton, MessageSelectMenu]] = components or []

    def to_dict(self):
        return {
            "type": self.type,
            "components": [component for component in self.components]
        }

    def add_components(self, components: List[Union[MessageButton, MessageSelectMenu]]):
        buttons = 0
        for component in components:
            if not component.custom_id:
                raise MissingCustomId(
                    f"You need to supply a custom id for the component {component}")

            if type(component) == MessageButton:
                buttons += 1

            elif buttons > 5:
                raise TooManyComponents("You can only have 5 buttons per row.")

            elif type(component) == MessageSelectMenu and buttons > 0:
                raise TooManyComponents(
                    "You can only have 1 select menu per row. No buttons along that select menu.")
            self.components.append(component.to_dict())
        return self

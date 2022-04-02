from .partials import PartialEmoji
from typing import Optional, List, Union
from .exceptions import InvalidArgumentType, CustomIdIsTooBig, TooManySelectMenuOptions, InvalidComponentStyle, TooManyComponents, MissingCustomId, LabelIsTooBig


class BaseComponent:
    """
    Base Component class, all components should inherit from this.
    Can be used to make new components which are yet to be covered by EpikCord.

    Attributes
    ----------
    custom_id: :class:`str`
        The custom id of the component. Used for `Client.component(custom_id)`.

    Parameters
    ----------
    custom_id: :class:`str`
        The custom id of the component. Used for `Client.component(custom_id)`.
    
    """
    def __init__(self, *, custom_id: str):
        self.custom_id: str = custom_id

    def set_custom_id(self, custom_id: str):
        """Sets the custom id of the component.

        Parameters:
            custom_id: :class:`str`
                The custom id of the component.

        Raises:
            InvalidArgumentType: If the Custom_ID is not a string.
            CustomIdIsTooBig: If the Custom_ID is bigger than 100 characters.
        """

        if not isinstance(custom_id, str):
            raise InvalidArgumentType("Custom Id must be a string.")

        elif len(custom_id) > 100:
            raise CustomIdIsTooBig("Custom Id must be 100 characters or less.")

        self.settings["custom_id"] = custom_id


class SelectMenuOption:
    """
    A class representation of a select menu option.
    This is for you to add to a ``SelectMenu`` via `SeletMenu.add_options`.

    Attributes
    ----------
    label: :class:`str`
        The label of the option.
    value: :class:`str`
        The value of the option.
    description: :class:`str`
        The description of the option.
    emoji: :class:`PartialEmoji`
        The emoji of the option.
    default: :class:`bool`
        Whether this option is added by default.

    Parameters
    ----------
    label: :class:`str`
        The label of the option.
    value: :class:`str`
        The value of the option.
    description: :class:`str`
        The description of the option.
    emoji: :class:`PartialEmoji`
        The emoji of the option.
    default: :class:`bool`
        Whether this option is added by default.

    """
    def __init__(self, label: str, value: str, description: Optional[str] = None, emoji: Optional[PartialEmoji] = None, default: Optional[bool] = None):
        self.label: str = label
        self.value: str = value
        self.description: Optional[str] = description
        self.emoji: Optional[PartialEmoji] = emoji
        self.default: Optional[bool] = default

    def to_dict(self):
        """
        Returns a dict representation of the option.
        """
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


class SelectMenu(BaseComponent):
    """
    A class representation of a select menu.
    
    Attributes
    ----------
    min_values: :class:`int`
        The minimum amount of values that can be selected.
    max_values: :class:`int`
        The maximum amount of values that can be selected.
    disabled: :class:`bool`
        Whether the select menu is disabled.
    custom_id: :class:`str`
        The custom id of the select menu. Used for `Client.component(custom_id)`.
    
    Parameters
    ----------
    min_values: :class:`int`
        The minimum amount of values that can be selected.
    max_values: :class:`int`
        The maximum amount of values that can be selected.
    disabled: :class:`bool`
        Whether the select menu is disabled.
    custom_id: :class:`str`
        The custom id of the select menu. Used for `Client.component(custom_id)`.
    """
    def __init__(self, *, min_values: Optional[int] = 1, max_values: Optional[int] = 1, disabled: Optional[bool] = False, custom_id: str, placeholder: Optional[str] = None):
        super().__init__(custom_id=custom_id)
        self.options: List[Union[SelectMenuOption, dict]] = []
        self.type: str = 3
        self.placeholder = placeholder
        self.min_values = min_values
        self.max_values = max_values
        self.disabled: bool = disabled

    def to_dict(self):
        """
        Returns a dict representation of the select menu.
        """
        payload = {
            "type": self.type,
            "options": self.options,
            "min_values": self.min_values,
            "max_values": self.max_values,
            "disabled": self.disabled,
            "custom_id": self.custom_id
        }

        if self.placeholder:
            payload["placeholder"] = self.placeholder
        
        return payload

    def add_options(self, options: List[SelectMenuOption]):
        """
        Adds options to the select menu.

        Parameters:
            options: :class:`List[SelectMenuOption]`
                The options to add.

        Raises:
            TooManySelectMenuOptions: If you reach 26 > options.

        """
        for option in options:

            if len(self.options) > 25:
                raise TooManySelectMenuOptions(
                    "You can only have 25 options in a select menu.")

            self.options.append(option.to_dict())
        return self

    def set_placeholder(self, placeholder: str):
        """
        Sets the placeholder of the select menu.

        Parameters:
            placeholder: :class:`str`
                The placeholder of the select menu.
        
        Raises:
            InvalidArgumentType: If the placeholder is not a string.
        """

        if not isinstance(placeholder, str):
            raise InvalidArgumentType("Placeholder must be a string.")

        self.placeholder = placeholder
        return self

    def set_min_values(self, min: int):
        """
        Set the minimum amount of values that can be selected.

        Parameters:
            min: :class:`int`
                The minimum amount of values that can be selected.

        Raises:
            InvalidArgumentType: If the min is not an integer.
        """
        if not isinstance(min, int):
            raise InvalidArgumentType("Min must be an integer.")

        self.min_values = min
        return self

    def set_max_values(self, max: int):
        """
        """
        if not isinstance(max, int):
            raise InvalidArgumentType("Max must be an integer.")

        self.max_values = max
        return self

    def set_disabled(self, disabled: bool):
        """
        Sets the disabled state of the select menu.

        Parameters:
            disabled: :class:`bool`
        
        Raises:
            InvalidArgumentType: If the disabled is not a boolean.
        """
        if not isinstance(disabled, bool):
            raise InvalidArgumentType("Disabled must be a boolean.")
        self.disabled = disabled


class TextInput(BaseComponent):
    """
    A class representation of a text input.
    Can only be used in a :class:`Modal`.

    Attributes
    ----------
    placeholder: :class:`str`
        The placeholder of the text input.
    max_length: :class:`int`
        The maximum length of the text input.
    disabled: :class:`bool`
        Whether the text input is disabled.
    custom_id: :class:`str`
        The custom id of the text input. Used for `Client.component(custom_id)`.
    
    """
    def __init__(self, *, custom_id: str, style: Union[int, str] = 1, label: str, min_length: Optional[int] = 1, max_length: Optional[int] = 4000, required: Optional[bool] = True, value: Optional[str] = None, placeholder: Optional[str] = None):
        super().__init__(custom_id=custom_id)
        VALID_STYLES = {
            "short": 1,
            "paragraph": 2
        }

        if isinstance(style, str):
            if style.lower() not in VALID_STYLES:
                raise InvalidComponentStyle("Style must be either 'Short' or 'Paragraph'.")
            style = VALID_STYLES[style.lower()]

        elif isinstance(style, int):
            if style not in VALID_STYLES.values():
                raise InvalidComponentStyle("Style must be either 1 or 2.")
        else:
            raise InvalidComponentStyle("Style must be an int or str.")

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
            "required": self.required
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


class Button(BaseComponent):
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


class ActionRow:
    def __init__(self, components: Optional[List[Union[Button, SelectMenu, TextInput]]] = None):
        self.type: int = 1
        self.components: List[Union[TextInput, Button, SelectMenu]] = components or []

    def to_dict(self):
        return {"type": self.type, "components": [component.to_dict() for component in self.components]}

    def add_components(self, components: List[Union[Button, SelectMenu]]):
        buttons = 0
        for component in components:
            if not component.custom_id:
                raise MissingCustomId(
                    f"You need to supply a custom id for the component {component}")

            if type(component) == Button:
                buttons += 1

            elif buttons > 5:
                raise TooManyComponents("You can only have 5 buttons per row.")

            elif isinstance(component, SelectMenu) and buttons > 0:
                raise TooManyComponents("You can only have 1 select menu per row. No buttons along that select menu.")
            self.components.append(component.to_dict())
        return self
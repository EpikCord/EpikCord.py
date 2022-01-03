from .abc import BaseComponent
from .partials import PartialEmoji
from .exceptions import TooManyComponents, InvalidMessageButtonStyle, CustomIdIsTooBig, InvalidArgumentType, TooManySelectMenuOptions, LabelIsTooBig
from typing import (
    Union,
    List
)


class MessageSelectMenuOption(BaseComponent):
    def __init__(self, **kwargs):
        self.data: dict = kwargs
        self.label: str = kwargs.get("label", "")
        self.value: str = kwargs.get("value", "")
        self.description: str = kwargs.get("description", "")
        self.emoji: PartialEmoji = kwargs.get("emoji", None)
        self.default: bool = kwargs.get("default", False)

class MessageButton(BaseComponent):
    def __init__(self):
        self.settings = {
            "type": 2,
            "style": 1,
            "label": "Click me!",
            "emoji": None,
            "disabled": False
        }
    
    def set_label(self, label: str):

        if not isinstance(label, str):
            raise InvalidArgumentType("Label must be a string.")
        
        if len(label) > 80:
            raise LabelIsTooBig("Label must be 80 characters or less.")
            
        self.settings["label"] = label
    
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
                raise InvalidMessageButtonStyle("Invalid button style. Style must be one of PRIMARY, SECONDARY, LINK, DANGER, or SUCCESS.")
            self.settings["style"] = style.upper()
            
        elif isinstance(style, int):
            if style not in valid_styles.values():
                raise InvalidMessageButtonStyle("Invalid button style. Style must be in range 1 to 5 inclusive.")
    
    def set_emoji(self, emoji: Union[PartialEmoji, dict]):

        if isinstance(emoji, dict):
            self.settings["emoji"] = emoji
            return

        elif isinstance(emoji, PartialEmoji):
            self.settings["emoji"] = emoji.data
            return
        raise InvalidArgumentType("Emoji must be a PartialEmoji or a dict that represents a PartialEmoji.")
                    
    def set_url(self, url: str):
        
        if not isinstance(url, str):
            raise InvalidArgumentType("Url must be a string.")
        
        self.settings["url"] = url
        self.settings["style"] = 5
        
        
class MessageSelectMenu:
    def __init__(self):
        self.settings = {
            "options": [], 
            "type": 3,
            "min_values": 1,
            "max_values": 1,
            "disabled": False
        }
            
    def add_options(self, options: List[MessageSelectMenuOption]):
        for option in options:
            
            if len(self.settings["options"] > 25):
                raise TooManySelectMenuOptions("You can only have 25 options in a select menu.")
            
            self.settings["options"].append(option.data)
        
    def set_placeholder(self, placeholder: str):
        if not isinstance(placeholder, str):
            raise InvalidArgumentType("Placeholder must be a string.")
        
        self.settings["placeholder"] = placeholder
    
    def set_min_values(self, min: int):
        if not isinstance(min, int):
            raise InvalidArgumentType("Min must be an integer.")
        
        self.options["min_values"] = min
        
    def set_max_values(self, max: int):
        if not isinstance(max, int):
            raise InvalidArgumentType("Max must be an integer.")
        
        self.options["max_values"] = max    

class MessageActionRow:
    def __init__(self):
        self.components = []
        
    def add_components(self, components: List[Union[MessageButton, MessageSelectMenu]]):
        buttons = 0
        for component in self.components:
            if type(component) == MessageButton:
                buttons += 1
            
            elif buttons >= 5:
                raise TooManyComponents("You can only have 5 buttons per row.")
            
            elif type(component) == MessageSelectMenu:
                raise TooManyComponents("You can only have 1 select menu per row. No buttons along that select menu.")
        self.components.append(components.settings)
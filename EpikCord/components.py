from .abc import BaseComponent
from .partials import PartialEmoji
from .exceptions import TooManyComponents, InvalidMessageButtonStyle, InvalidArgumentType, TooManySelectMenuOptions, LabelIsTooBig
from typing import (
    Union,
    List,
    Optional
)

class MessageSelectMenuOption:
    def __init__(self, label: str, value: str, description: Optional[str], emoji: Optional[PartialEmoji], default: Optional[bool]):
        self.settings = {
            "label": label,
            "value": value,
            "description": description or None,
            "emoji": emoji or None,
            "default": default or None            
        }
    
    def __repr__(self):
        return self.settings

class MessageSelectMenu(BaseComponent):
    def __init__(self):
        self.settings = {
            "options": [], 
            "type": 3,
            "min_values": 1,
            "max_values": 1,
            "disabled": False
        }
    
    def __repr__(self):
        return self.settings

    def add_options(self, options: List[MessageSelectMenuOption]):
        for option in options:
            
            if len(self.settings["options"] > 25):
                raise TooManySelectMenuOptions("You can only have 25 options in a select menu.")
            
            self.settings["options"].append(option.data)
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


class MessageButton(BaseComponent):
    def __init__(self,*, style: Optional[Union[int, str]] = 1, label: Optional[str], emoji: Optional[Union[PartialEmoji, dict]], url: Optional[str]):
        self.settings = {
            "type": 2,
            "style": style or 1,
            "label": label or "Click me!",
            "emoji": None,
            "disabled": False,
        }
        if url:
            self.settings["url"] = url
            self.settings["style"] = 5
        if emoji:
            self.settings["emoji"] = emoji
    def __repr__(self):
        return self.settings

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
                raise InvalidMessageButtonStyle("Invalid button style. Style must be one of PRIMARY, SECONDARY, LINK, DANGER, or SUCCESS.")
            self.settings["style"] = valid_styles[style.upper()]
            return self
            
        elif isinstance(style, int):
            if style not in valid_styles.values():
                raise InvalidMessageButtonStyle("Invalid button style. Style must be in range 1 to 5 inclusive.")
            self.settings["style"] = style
            return self
    def set_emoji(self, emoji: Union[PartialEmoji, dict]):

        if isinstance(emoji, dict):
            self.settings["emoji"] = emoji
            return self

        elif isinstance(emoji, PartialEmoji):
            self.settings["emoji"] = emoji.data
            return self
        raise InvalidArgumentType("Emoji must be a PartialEmoji or a dict that represents a PartialEmoji.")
                    
    def set_url(self, url: str):
        
        if not isinstance(url, str):
            raise InvalidArgumentType("Url must be a string.")
        
        self.settings["url"] = url
        self.settings["style"] = 5
        return self

        

class MessageActionRow:
    def __init__(self, components: Optional[List[Union[MessageButton, MessageSelectMenu]]]):
        self.settings = {
            "type": 1,
            "components": components
        }

    def __repr__(self):
        return self.settings
        
    def add_components(self, components: List[Union[MessageButton, MessageSelectMenu]]):
        buttons = 0
        for component in self.settings["components"]:
            if type(component) == MessageButton:
                buttons += 1
            
            elif buttons >= 5:
                raise TooManyComponents("You can only have 5 buttons per row.")
            
            elif type(component) == MessageSelectMenu:
                raise TooManyComponents("You can only have 1 select menu per row. No buttons along that select menu.")
        self.settings["components"].append(components)
        return self
from .exceptions import TooManyComponents, InvalidMessageButtonStyle
from typing import (
    Union
)

class MessageButton:
    def __init__(self):
        self.settings = {}
    
    def set_label(self, label: str):
        self.settings["label"] = label
    
    def set_style(self, style: Union[int, str]):
        if isinstance(style, str):
            if style.upper() not in ["PRIMARY", "SECONDARY", "LINK", "DANGER", "SUCCESS"]:
                raise InvalidMessageButtonStyle("Invalid button style. Style must be one of PRIMARY, SECONDARY, LINK, DANGER, or SUCCESS.")
            self.settings["style"] = style.upper()
            
        elif isinstance(style, int):
            if style not in range(5):
                raise InvalidMessageButtonStyle("Invalid button style. Style must be in range 1 to 5 inclusive.")
            

class MessageSelectMenu:
    def __init__(self):
        self.settings = {"options": []}


class MessageActionRow:
    def __init__(self):
        self.current_components = []
        
    def add_components(self, components: Union[MessageButton, MessageSelectMenu]):
        buttons = 0
        for component in self.current_components:
            if type(component) == MessageButton:
                buttons += 1
            
            elif buttons >= 5:
                raise TooManyComponents("You can only have 5 buttons per row.")
            
            elif type(component) == MessageSelectMenu:
                raise TooManyComponents("You can only have 1 select menu per row. No buttons along that select menu.")
        self.current_components.append(component)
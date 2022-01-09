from .abc import BaseSlashCommandOption
from typing import (
    Optional,
    List
)

class Section:
    def __init__(self):
        self.commands = {}
        self.events = {}
    
    def event(self, event_name: str):
        def register_event(func):
            self.events[event_name] = func
        return register_event

    def slash_command(self,*, name: str, description: Optional[str], options: List[BaseSlashCommandOption]):
        def register_slash_command(func):
            self.commands[name] = {
                "callback": func,
                "name": name,
                "description": description,
                "options": options
            }
        return register_slash_command
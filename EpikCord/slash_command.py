from typing import (
    Optional
)

class SlashCommand: # Somethin like Command from commands.ext dpy
    def __init__(self, data: dict):
        self.name: str = data["name"]
        self.description: Optional[str] = data["description"]
        self.options
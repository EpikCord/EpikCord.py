from .colours import Colour
from typing import (
    Optional,
    List
)

class EmbedAuthor:
    def __init__(self, data: dict):
        self.name: str = data["name"]
        self.url: Optional[str] = data["url"] or None
        self.icon_url: Optional[str] = data["icon_url"] or None
        self.proxy_icon_url: Optional[str] = data["proxy_icon_url"] or None

class Embed: # Always wanted to make this class :D
    def __init__(self, data: dict):
        self.data = data
        self.title: Optional[str] = data["title"] or None
        self.type: Optional[str] = data["type"] or None
        self.description: Optional[str] = data["description"] or None
        self.url: Optional[str] = data["url"] or None
        self.timestamp: Optional[str] = data["timestamp"] or None
        self.color: Optional[Colour] = data["color"] or None
        self.footer: Optional[str] = data["footer"] or None
        self.image: Optional[str] = data["image"] or None
        self.thumbnail: Optional[str] = data["thumbnail"] or None
        self.valid_styles: Optional[str] = data["valid_styles"] or None
        self.provider: Optional[str] = data["provider"] or None
        self.author: Optional[EmbedAuthor] = EmbedAuthor(data["author"]) or None
        self.fields: Optional[List[str]] = data["fields"] or None
        
    def add_field(self, name: str, value: str, inline: bool):
        self.fields.append({"name": name, "value": value, "inline": inline})
        
    def set_title(self, title: str):
        self.title = title
    
    def set_description(self, description: str):
        self.description = description
    
    # Someone else do this icba
import datetime
from .color import Colour
from typing import Optional, List


class Embed:  # Always wanted to make this class :D
    def __init__(self, *,
        title: Optional[str] = None,
        description: Optional[str] = None,
        color: Optional[Colour] = None,
        video: Optional[dict] = None,
        timestamp: Optional[datetime.datetime] = None,
        colour: Optional[Colour] = None,
        url: Optional[str] = None,
        type: Optional[int] = None,
        footer: Optional[dict] = None,
        image: Optional[dict] = None,
        thumbnail: Optional[dict] = None,
        provider: Optional[dict] = None,
        author: Optional[dict] = None,
        fields: Optional[List[dict]] = None,
                 ):
        self.type: int = type
        self.title: Optional[str] = title
        self.type: Optional[str] = type
        self.description: Optional[str] = description
        self.url: Optional[str] = url
        self.video: Optional[dict] = video
        self.timestamp: Optional[str] = timestamp
        self.color: Optional[Colour] = color or colour
        self.footer: Optional[str] = footer
        self.image: Optional[str] = image
        self.thumbnail: Optional[str] = thumbnail
        self.provider: Optional[str] = provider
        self.author: Optional[dict] = author
        self.fields: Optional[List[str]] = fields

    def add_field(self, *, name: str, value: str, inline: bool = False):
        self.fields.append({"name": name, "value": value, "inline": inline})

    def set_thumbnail(self, *, url: Optional[str] = None, proxy_url: Optional[str] = None, height: Optional[int] = None, width: Optional[int] = None):
        config = {
            "url": url
        }
        if proxy_url:
            config["proxy_url"] = proxy_url
        if height:
            config["height"] = height
        if width:
            config["width"] = width

        self.thumbnail = config

    def set_video(self, *, url: Optional[str] = None, proxy_url: Optional[str] = None, height: Optional[int] = None, width: Optional[int] = None):
        config = {
            "url": url
        }
        if proxy_url:
            config["proxy_url"] = proxy_url
        if height:
            config["height"] = height
        if width:
            config["width"] = width

        self.video = config

    def set_image(self, *, url: Optional[str] = None, proxy_url: Optional[str] = None, height: Optional[int] = None, width: Optional[int] = None):
        config = {
            "url": url
        }
        if proxy_url:
            config["proxy_url"] = proxy_url
        if height:
            config["height"] = height
        if width:
            config["width"] = width

        self.image = config

    def set_provider(self, *, name: Optional[str] = None, url: Optional[str] = None):
        config = {}
        if url:
            config["url"] = url
        if name:
            config["name"] = name
        self.provider = config

    def set_footer(self, *, text: Optional[str], icon_url: Optional[str] = None, proxy_icon_url: Optional[str] = None):
        payload = {}
        if text:
            payload["text"] = text
        if icon_url:
            payload["icon_url"] = icon_url
        if proxy_icon_url:
            payload["proxy_icon_url"] = proxy_icon_url
        self.footer = payload

    def set_author(self, name: Optional[str] = None, url: Optional[str] = None, icon_url: Optional[str] = None, proxy_icon_url: Optional[str] = None):
        payload = {}
        if name:
            payload["name"] = name
        if url:
            payload["url"] = url
        if icon_url:
            payload["icon_url"] = icon_url
        if proxy_icon_url:
            payload["proxy_icon_url"] = proxy_icon_url

        self.author = payload

    def set_fields(self, *, fields: List[dict]):
        self.fields = fields

    def set_color(self, *, colour: Colour):
        self.color = colour.value

    def set_timestamp(self, *, timestamp: datetime.datetime):
        self.timestamp = timestamp.isoformat()

    def set_title(self, title: Optional[str] = None):
        self.title = title

    def set_description(self, description: Optional[str] = None):
        self.description = description

    def set_url(self, url: Optional[str] = None):
        self.url = url

    def to_dict(self):
        final_product = {}

        if getattr(self, "title"):
            final_product["title"] = self.title
        if getattr(self, "description"):
            final_product["description"] = self.description
        if getattr(self, "url"):
            final_product["url"] = self.url
        if getattr(self, "timestamp"):
            final_product["timestamp"] = self.timestamp
        if getattr(self, "color"):
            final_product["color"] = self.color
        if getattr(self, "footer"):
            final_product["footer"] = self.footer
        if getattr(self, "image"):
            final_product["image"] = self.image
        if getattr(self, "thumbnail"):
            final_product["thumbnail"] = self.thumbnail
        if getattr(self, "video"):
            final_product["video"] = self.video
        if getattr(self, "provider"):
            final_product["provider"] = self.provider
        if getattr(self, "author"):
            final_product["author"] = self.author
        if getattr(self, "fields"):
            final_product["fields"] = self.fields

        return final_product

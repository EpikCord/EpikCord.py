from typing import (
    Optional
)
class Attachment:
    def __init__(self, data: dict):
        self.id: str = data["id"]
        self.file_name: str = data["filename"]
        self.description: Optional[str] = data["description"] or None
        self.content_type: Optional[str] = data["content_type"] or None
        self.size: int = data["size"]
        self.proxy_url: str = data["proxy_url"]
        self.width: Optional[int] = data["width"] or None
        self.height: Optional[int] = data["height"] or None
        self.ephemeral: Optional[bool] = data["ephemeral"] or None
from typing import Optional, List
class PartialUser:
    def __init__(self, data: dict):
        self.data: dict = data
        self.id: str = data.get("id")
        self.username: str = data.get("username")
        self.discriminator: str = data.get("discriminator")
        self.avatar: Optional[str] = data.get("avatar")


class PartialGuild:
    def __init__(self, data):
        self.data: dict = data
        self.id: str = data.get("id")
        self.name: str = data.get("name")
        self.permissions: int = int(data.get("permissions"))
        self.features: List[str] = data.get("features")


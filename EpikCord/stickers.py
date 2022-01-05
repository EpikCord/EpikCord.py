class StickerItem:
    def __init__(self, data: dict):
        self.id: str = data["id"]
        self.name: str = data["name"]
        self.format_type: int = data["format_type"]
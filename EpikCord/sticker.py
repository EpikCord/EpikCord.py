class StickerItem:
    def __init__(self, data : dict):
        self.id: str = data.get("id")
        self.name: str = data.get("name")
        self.format_type: int = data.get("format_type")

class Sticker(StickerItem):
    def __init__(self, data: dict):
        super().__init__(data)
        self.description: str = data.get("description")
        self.tags: str = data.get("tags")
        self.type: str = data.get("image")
        self.pack_id: int = data.get("pack_id")
        self.sort_value: int = data.get("sort_value")


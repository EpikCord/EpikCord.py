import io
import mimetypes
from typing import Optional

from discord_typings import AttachmentData

from .client import Client
from .exceptions import UnknownMimeType


class Attachment:
    def __init__(self, data: AttachmentData):
        self.id = int(data["id"])
        self.filename = data["filename"]
        self.size = data["size"]
        self.url = data["url"]
        self.proxy_url = data["proxy_url"]
        self.description = data.get("description")
        self.content_type = data.get("content_type")
        self.height = data.get("height")
        self.width = data.get("width")
        self.ephemeral = data.get("ephemeral")
        self._data = data


class File:
    def __init__(
        self,
        filename: str,
        contents: io.IOBase,
        *,
        description: Optional[str] = None,
        mime_type: Optional[str] = None,
        spoiler: bool = False,
    ):
        """
        Parameters
        ----------
        filename: str
            The filename of the file.
        contents: io.IOBase
            The contents of the file.
        mime_type: Optional[str]
            The mime type of the file. If not provided, it will be guessed.
        spoiler: bool
            Whether the file is a spoiler.
        description: Optional[str]
            The description of the file.
        """
        self.contents: io.IOBase = contents
        self.mime_type = mime_type or _guess_mime_type(filename)

        if self.mime_type is None:
            raise UnknownMimeType(filename)

        if spoiler:
            self.filename = f"SPOILER_{filename}"
        else:
            self.filename = filename
        self.description: Optional[str] = description


def _guess_mime_type(filename: str) -> Optional[str]:
    mime_type, _encoding = mimetypes.guess_type(filename)
    return mime_type

import io
import mimetypes
from typing import Optional

from .exceptions import UnknownMimeType


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

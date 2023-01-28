import io
import mimetypes
from typing import Optional


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
            Whether or not the file is a spoiler.
        ephemeral: bool
            Whether or not the file is ephemeral.
        description: Optional[str]
            The description of the file.
        """
        self.contents: io.IOBase = contents
        self.mime_type: Optional[str] = mime_type or mimetypes.guess_type(filename)[0]
        if spoiler:
            self.filename = f"SPOILER_{filename}"
        else:
            self.filename = filename
        self.description: Optional[str] = description

import io
import mimetypes
from typing import Optional

from discord_typings import AttachmentData

from .exceptions import UnknownMimeType


class Attachment:
    """
    Attributes:
    ----------
    id: :class:`int`
        The id of the attachment.
    filename: :class:`str`
        The name of the attachment.
    size: :class:``
        The size of the attachment.
    url: :class:`str`
        The url to the attachment.
    proxy_url: :class:`str`
        The proxy url to the attachment.
    description: :class:`str`
        The description of the attachment.
    content_type: :class:``
        ...
    height: :class:`int`
        The height of the attachment.
    width: :class:`int`
        The width of the attachment.
    ephemeral: :class:`bool`
        If the file was sent with an ephemeral.
    _data: :class:`discord_typings.AttachmentData`
        The data containing all the information of the file.
    """
    def __init__(self, data: AttachmentData):
        """
        Parameters:
        ----------
        data: :class:`discord_typings.AttachmentData`
            The data containing all the information of the file.
        """

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
    """
    Attributes:
    ----------
    filename: :class:`str`
        The name of the file.
    contents: :class:`io.IOBase`
        The bytes inside the file.
    description: Optional[str]
        The description of the file.
    mine_type: :class:`str`
        ...
    spolier (optional): :class:`bool`
        If the file is sent with a spolier.
    """
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
        mime_type: str
            The mime type of the file. If not provided, it will be guessed.
        spoiler: bool
            Whether the file is a spoiler.
        description: Optional[str]
            The description of the file.

        Raises:
        ------
        UnkownMineType: When mine type is None
        """
        self.contents: io.IOBase = contents
        self.mime_type = mime_type or _guess_mime_type(filename)

        if self.mime_type is None:
            raise UnknownMimeType(filename)

        self.filename = f"SPOILER_{filename}" if spoiler else filename
        self.description: Optional[str] = description


def _guess_mime_type(filename: str) -> Optional[str]:
    """
    Parameters:
    ----------
    filename: :class:`str`
        The name of the file
    
    Returns:
    -------
    mine_type: :class:``
        ...
    """
    mime_type, _encoding = mimetypes.guess_type(filename)
    return mime_type

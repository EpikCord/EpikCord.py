import os
import io 
from typing import Optional, Union


class File:
    """
    Represents a file. Sourced from Discord.py
    """
    def __init__(
        self,
        fp: Union[str, bytes, os.PathLike, io.BufferedIOBase],
        filename: Optional[str] = None,
        *,
        spoiler: bool = False,
    ):
        if isinstance(fp, io.IOBase):
            if not (fp.seekable() and fp.readable()):
                raise ValueError(f'File buffer {fp!r} must be seekable and readable')
            self.fp = fp
            self._original_pos = fp.tell()
        else:
                self.fp = open(fp, 'rb')
                self._original_pos = 0
        self._closer = self.fp.close
        self.fp.close = lambda: None
        
        if filename is None:
            if isinstance(fp, str):
                _, self.filename = os.path.split(fp)
            else:
                self.filename = getattr(fp, 'name', None)
        else:
            self.filename = filename
        if spoiler and self.filename is not None and not self.filename.startswith('SPOILER_'):
            self.filename = 'SPOILER_' + self.filename

            self.spoiler = spoiler or (self.filename is not None and self.filename.startswith('SPOILER_'))

        def reset(self, *, seek: Union[int, bool] = True) -> None:
            if seek:
                self.fp.seek(self._original_pos)

        def close(self) -> None:
            self.fp.close = self._closer
            self._closer()

class Attachment:
    def __init__(self, data: dict):
        self.id: str = data.get("id")
        self.file_name: str = data.get("filename")
        self.description: Optional[str] = data.get("description")
        self.content_type: Optional[str] = data.get("content_type")
        self.size: int = data.get("size")
        self.url: str = data.get("url")
        self.proxy_url: str = data.get("proxy_url")
        self.width: Optional[int] = data.get("width")
        self.height: Optional[int] = data.get("height")
        self.ephemeral: Optional[bool] = data.get("ephemeral")

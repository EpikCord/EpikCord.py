from typing import (
    Optional,
    List
)
from .message import Message
from .partials import PartialUser
from .exceptions import InvalidArgumentType
from base64 import b64encode

def _get_mime_type_for_image(data: bytes):
    if data.startswith(b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A'):
        return 'image/png'
    elif data[0:3] == b'\xff\xd8\xff' or data[6:10] in (b'JFIF', b'Exif'):
        return 'image/jpeg'
    elif data.startswith((b'\x47\x49\x46\x38\x37\x61', b'\x47\x49\x46\x38\x39\x61')):
        return 'image/gif'
    elif data.startswith(b'RIFF') and data[8:12] == b'WEBP':
        return 'image/webp'
    else:
        raise InvalidArgumentType('Unsupported image type given')


def _bytes_to_base64_data(data: bytes) -> str:
    fmt = 'data:{mime};base64,{data}'
    mime = _get_mime_type_for_image(data)
    b64 = b64encode(data).decode('ascii')
    return fmt.format(mime=mime, data=b64)



class User:
    def __init__(self, client, data: dict):
        self.data = data
        self.id: str = data["id"]
        self.username: str = data["username"]
        self.discriminator: str = data["discriminator"]
        self.avatar: Optional[str] = data["avatar"]
        self.client = client
        self.bot: bool = data["bot"]
        self.system: bool = data["system"]
        self.mfa_enabled: bool = data["mfa_enabled"]
        self.banner: Optional[str] = data["banner"] or None
        self.accent_color: Optional[int] = data["accent_color"] or None # the user's banner color encoded as an integer representation of hexadecimal color code	
        self.locale: Optional[str] = data["locale"] or None
        self.verified: bool = data["verified"]
        self.email: Optional[str] = data["email"] or None
        self.flags: int = data["flags"]
        self.premium_type: int = data["premium_type"]
        self.public_flags: int = data["public_flags"]

    async def fetch_messages(self,*, around: Optional[str] = None, before: Optional[str] = None, after: Optional[str] = None, limit: Optional[int] = None) -> List[Message]:
        response = await self.client.http.get(f"channels/{self.id}/messages", params={"around": around, "before": before, "after": after, "limit": limit})
        data = await response.json()
        return [Message(message) for message in data]
    
    async def fetch_message(self,*, message_id: str) -> Message:
        response = await self.client.http.get(f"channels/{self.id}/messages/{message_id}")
        data = await response.json()
        return Message(data)

    async def send(self, message_data: dict) -> Message:
        response = await self.client.http.post(f"channels/{self.id}/messages", form=message_data)
        return Message(await response.json())

class ClientUser(User):
    
    def __init__(self, data: dict):
        super().__init__(data)
    
    async def fetch(self):
        response = await self.client.http.get("users/@me")
        data = await response.json()
        super().__init__(data) # Reinitialse the class with the new data.
    
    async def edit(self, *, username: Optional[str] = None, avatar: Optional[bytes] = None):
        payload = {}
        if username:
            payload["username"] = username
        if avatar:
            payload["avatar"] = _bytes_to_base64_data(avatar)
        response = await self.client.http.patch("users/@me", json=payload)
        data = await response.json()
        self.__init__(data) # Reinitialse the class with the new data, the full data.

    async def fetch_messages(self):
        raise NotImplementedError("ClientUser.fetch_messages() is not valid for the client user.")

    async def fetch_message(self):
        raise NotImplementedError("ClientUser.fetch_message() is not valid for the client user.")

    async def send(self):
        raise NotImplementedError("ClientUser.send() is not valid for the client user.")

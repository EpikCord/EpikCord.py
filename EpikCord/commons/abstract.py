from ..core import Message, Button, SelectMenu, TextInput, ActionRow, User, Modal
from typing import (
    Optional,
    List,
    Union
)

class Messageable:
    def __init__(self, client, channel_id: str):
        self.id: str = channel_id
        self.client = client

    async def fetch_messages(
        self,
        *,
        around: Optional[str] = None,
        before: Optional[str] = None,
        after: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> List[Message]:
        response = await self.client.http.get(
            f"channels/{self.id}/messages",
            params={"around": around, "before": before, "after": after, "limit": limit},
        )
        data = await response.json()
        return [Message(self.client, message) for message in data]

    async def fetch_message(self, *, message_id: str) -> Message:
        response = await self.client.http.get(
            f"channels/{self.id}/messages/{message_id}"
        )
        data = await response.json()
        return Message(self.client, data)

    async def send(
        self,
        content: Optional[str] = None,
        *,
        embeds: Optional[List[dict]] = None,
        components=None,
        tts: Optional[bool] = False,
        allowed_mentions=None,
        sticker_ids: Optional[List[str]] = None,
        attachments: List[File] = None,
        suppress_embeds: bool = False,
    ) -> Message:
        payload = {}

        if content:
            payload["content"] = content

        if embeds:
            payload["embeds"] = [embed.to_dict() for embed in embeds]

        if components:
            payload["components"] = [component.to_dict() for component in components]

        if tts:
            payload["tts"] = tts

        if allowed_mentions:
            payload["allowed_mentions"] = allowed_mentions.to_dict()

        if sticker_ids:
            payload["sticker_ids"] = sticker_ids

        if attachments:
            payload["attachments"] = [
                attachment.to_dict() for attachment in attachments
            ]

        if suppress_embeds:
            payload["suppress_embeds"] = 1 << 2

        response = await self.client.http.post(
            f"channels/{self.id}/messages", json=payload
        )
        data = await response.json()
        return Message(self.client, data)

class BaseInteraction:
    def __init__(self, client, data: dict):
        self.id: str = data.get("id")
        self.client = client
        self.type: int = data.get("type")
        self.application_id: int = data.get("application_id")
        self.data: dict = data
        self.interaction_data: Optional[dict] = data.get("data")
        self.guild_id: Optional[str] = data.get("guild_id")
        self.channel_id: Optional[str] = data.get("channel_id")
        self.author: Optional[Union[User, GuildMember]] = (
            GuildMember(client, data.get("member"))
            if data.get("member")
            else User(client, data.get("user"))
            if data.get("user")
            else None
        )
        self.token: str = data.get("token")
        self.version: int = data.get("version")
        self.locale: Optional[str] = data.get("locale")
        self.guild_locale: Optional[str] = data.get("guild_locale")
        self.original_response: Optional[
            Message
        ] = None  # Can't be set on construction.
        self.followup_response: Optional[
            Message
        ] = None  # Can't be set on construction.

    async def reply(
        self,
        *,
        tts: bool = False,
        content: Optional[str] = None,
        embeds: Optional[List[Embed]] = None,
        allowed_mentions=None,
        components: Optional[List[ActionRow]] = None,
        attachments: Optional[List[Attachment]] = None,
        suppress_embeds: Optional[bool] = False,
        ephemeral: Optional[bool] = False,
    ) -> None:

        message_data = {"tts": tts, "flags": 0}

        if suppress_embeds:
            message_data["flags"] | +1 << 2
        if ephemeral:
            message_data["flags"] |= 1 << 6

        if content:
            message_data["content"] = content
        if embeds:
            message_data["embeds"] = [embed.to_dict() for embed in embeds]
        if allowed_mentions:
            message_data["allowed_mentions"] = allowed_mentions.to_dict()
        if components:
            message_data["components"] = [
                component.to_dict() for component in components
            ]
        if attachments:
            message_data["attachments"] = [
                attachment.to_dict() for attachment in attachments
            ]

        payload = {"type": 4, "data": message_data}
        await self.client.http.post(
            f"/interactions/{self.id}/{self.token}/callback", json=payload
        )

    async def defer(self, *, show_loading_state: Optional[bool] = True):
        if show_loading_state:
            return await self.client.http.post(
                f"/interaction/{self.id}/{self.token}/callback", json={"type": 5}
            )
        else:
            return await self.client.http.post(
                f"/interaction/{self.id}/{self.token}/callback", json={"type": 6}
            )

    async def send_modal(self, modal: Modal):
        if not isinstance(modal, Modal):

            raise TypeError(f"The modal argument must be of type Modal not {modal.__class__}.")

        payload = {"type": 9, "data": modal.to_dict()}
        await self.client.http.post(
            f"/interactions/{self.id}/{self.token}/callback", json=payload
        )

    @property
    def is_ping(self):
        return self.type == 1

    @property
    def is_application_command(self):
        return self.type == 2

    @property
    def is_message_component(self):
        return self.type == 3

    @property
    def is_autocomplete(self):
        return self.type == 4

    @property
    def is_modal_submit(self):
        return self.type == 5

    async def fetch_original_response(self, *, skip_cache: Optional[bool] = False):
        if not skip_cache and self.original_response:
            return self.original_response
        message_data = await self.client.http.get(
            f"/webhooks/{self.application_id}/{self.token}/messages/@original"
        )
        self.original_response = Message(self.client, message_data)
        return self.original_response

    async def edit_original_response(
        self,
        *,
        tts: bool = False,
        content: Optional[str] = None,
        embeds: Optional[List[Embed]] = None,
        allowed_mentions=None,
        components: Optional[List[Union[Button, SelectMenu, TextInput]]] = None,
        attachments: Optional[List[Attachment]] = None,
        suppress_embeds: Optional[bool] = False,
        ephemeral: Optional[bool] = False,
    ) -> None:

        message_data = {"tts": tts, "flags": 0}

        if suppress_embeds:
            message_data["flags"] += 1 << 2
        if ephemeral:
            message_data["flags"] += 1 << 6

        if content:
            message_data["content"] = content
        if embeds:
            message_data["embeds"] = [embed.to_dict() for embed in embeds]
        if allowed_mentions:
            message_data["allowed_mentions"] = allowed_mentions.to_dict()
        if components:
            message_data["components"] = [
                component.to_dict() for component in components
            ]
        if attachments:
            message_data["attachments"] = [
                attachment.to_dict() for attachment in attachments
            ]

        new_message_data = await self.client.http.patch(
            f"/webhooks/{self.application_id}/{self.token}/messages/@original",
            json=message_data,
        )
        self.original_response = Message(self.client, new_message_data)
        return self.original_response

    async def delete_original_response(self):
        await self.client.http.delete(
            f"/webhooks/{self.application_id}/{self.token}/messages/@original"
        )

    async def create_followup(
        self,
        *,
        tts: bool = False,
        content: Optional[str] = None,
        embeds: Optional[List[Embed]] = None,
        allowed_mentions=None,
        components: Optional[List[Union[Button, SelectMenu, TextInput]]] = None,
        attachments: Optional[List[Attachment]] = None,
        suppress_embeds: Optional[bool] = False,
        ephemeral: Optional[bool] = False,
    ) -> None:

        message_data = {"tts": tts, "flags": 0}

        if suppress_embeds:
            message_data["flags"] += 1 << 2
        if ephemeral:
            message_data["flags"] += 1 << 6

        if content:
            message_data["content"] = content
        if embeds:
            message_data["embeds"] = [embed.to_dict() for embed in embeds]
        if allowed_mentions:
            message_data["allowed_mentions"] = allowed_mentions.to_dict()
        if components:
            message_data["components"] = [
                component.to_dict() for component in components
            ]
        if attachments:
            message_data["attachments"] = [
                attachment.to_dict() for attachment in attachments
            ]

        response = await self.client.http.post(
            f"/webhooks/{self.application_id}/{self.token}", json=message_data
        )
        new_message_data = await response.json()
        self.followup_response = Message(self.client, new_message_data)
        return self.followup_response

    async def edit_followup(
        self,
        *,
        tts: bool = False,
        content: Optional[str] = None,
        embeds: Optional[List[Embed]] = None,
        allowed_mentions=None,
        components: Optional[List[Union[Button, SelectMenu, TextInput]]] = None,
        attachments: Optional[List[Attachment]] = None,
        suppress_embeds: Optional[bool] = False,
        ephemeral: Optional[bool] = False,
    ) -> None:

        message_data = {"tts": tts, "flags": 0}

        if suppress_embeds:
            message_data["flags"] += 1 << 2
        if ephemeral:
            message_data["flags"] += 1 << 6

        if content:
            message_data["content"] = content
        if embeds:
            message_data["embeds"] = [embed.to_dict() for embed in embeds]
        if allowed_mentions:
            message_data["allowed_mentions"] = allowed_mentions.to_dict()
        if components:
            message_data["components"] = [
                component.to_dict() for component in components
            ]
        if attachments:
            message_data["attachments"] = [
                attachment.to_dict() for attachment in attachments
            ]

        await self.client.http.patch(
            f"/webhook/{self.application_id}/{self.token}/", json=message_data
        )

    async def delete_followup(self):
        return await self.client.http.delete(
            f"/webhook/{self.application_id}/{self.token}/"
        )
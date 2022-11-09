from __future__ import annotations

import asyncio
import datetime
import re
from base64 import b64encode
from collections import defaultdict
from logging import getLogger
from typing import TYPE_CHECKING, Callable, Optional, TypeVar, Union

from ..channels import *
from ..components import *
from ..exceptions import InvalidArgumentType
from ..interactions import (
    ApplicationCommandInteraction,
    AutoCompleteInteraction,
    ButtonInteraction,
    ModalSubmitInteraction,
    SelectMenuInteraction,
)
from ..thread import Thread

if TYPE_CHECKING:
    import discord_typings

    from ..client import WebsocketClient

logger = getLogger(__name__)
T = TypeVar("T")


class Utils:
    """
    A utility class, used to make difficult things easy.

    Attributes:
    -----------
    client: Client
        The client that this utility class is attached to.

    """

    channels_types = {
        0: GuildTextChannel,
        1: DMChannel,
        2: VoiceChannel,
        4: CategoryChannel,
        5: GuildAnnouncementChannel,
        10: Thread,
        11: Thread,
        13: GuildStageChannel,
    }

    def __init__(self, client: WebsocketClient):
        self.client: WebsocketClient = client
        self._MARKDOWN_ESCAPE_SUBREGEX = "|".join(
            r"\{0}(?=([\s\S]*((?<!\{0})\{0})))".format(c)
            for c in ("*", "`", "_", "~", "|")
        )

        self._MARKDOWN_ESCAPE_COMMON = r"^>(?:>>)?\s|\[.+\]\(.+\)"

        self._MARKDOWN_ESCAPE_REGEX = re.compile(
            rf"(?P<markdown>{self._MARKDOWN_ESCAPE_SUBREGEX}|{self._MARKDOWN_ESCAPE_COMMON})",
            re.MULTILINE,
        )

        self._URL_REGEX = (
            r"(?P<url><[^: >]+:\/[^ >]+>|(?:https?|steam):\/\/[^\s<]+[^<.,:;\"\'\]\s])"
        )

        self._MARKDOWN_STOCK_REGEX = (
            rf"(?P<markdown>[_\\~|\*`]|{self._MARKDOWN_ESCAPE_COMMON})"
        )

    @staticmethod
    def filter_values(dictionary: dict):
        return {k: v for k, v in dictionary.items() if v is not None}

    async def override_commands(self):
        command_sorter = defaultdict(list)

        for command in self.client.commands.values():
            command_payload = {"name": command.name, "type": command.type}

            if command_payload["type"] == 1:
                command_payload["description"] = command.description
                command_payload["options"] = [
                    option.to_dict() for option in command.options
                ]

                if command.name_localizations:
                    command_payload["name_localizations"] = {}
                    for name_localization in command.name_localizations:
                        if not name_localization:
                            return
                        command_payload["name_localizations"][
                            name_localization
                        ] = name_localization.to_dict()

                if command.description_localizations:
                    command_payload["description_localizations"] = {}
                    for description_localization in command.description_localizations:
                        if not description_localization:
                            return
                        command_payload["description_localizations"][
                            description_localization
                        ] = description_localization.to_dict()

            if command.guild_ids:
                for guild_id in command.guild_ids:
                    command_sorter[guild_id].append(command_payload)
            else:
                command_sorter["global"].append(command_payload)

        for guild_id, commands in command_sorter.items():
            if guild_id == "global":
                await self.client.application.bulk_overwrite_global_application_commands(
                    commands
                )
                continue

            await self.client.application.bulk_overwrite_guild_application_commands(
                guild_id, commands
            )

    @staticmethod
    def get_mime_type_for_image(data: bytes) -> str:
        if data.startswith(b"\x89\x50\x4E\x47\x0D\x0A\x1A\x0A"):
            return "image/png"

        if data[:3] == b"\xff\xd8\xff" or data[6:10] in (b"JFIF", b"Exif"):
            return "image/jpeg"

        gif_header = (b"\x47\x49\x46\x38\x37\x61", b"\x47\x49\x46\x38\x39\x61")
        if data.startswith(gif_header):
            return "image/gif"

        if data.startswith(b"RIFF") and data[8:12] == b"WEBP":
            return "image/webp"

        raise InvalidArgumentType("Unsupported image type given")

    @staticmethod
    def bytes_to_base64_data(data: bytes) -> str:
        fmt = "data:{mime};base64,{data}"
        mime = Utils.get_mime_type_for_image(data)
        b64 = b64encode(data).decode("ascii")
        return fmt.format(mime=mime, data=b64)

    @staticmethod
    def component_from_type(component_data: dict):
        component_types = [Button, SelectMenu, TextInput]
        component_type = component_data["type"]

        if component_type < 2 or component_type > 4:
            logger.warning(f"Unknown component type: {component_type}")
            return

        component_cls = component_types[component_type - 2]
        return component_cls(**component_data)

    @staticmethod
    def filter_values_dynamic(check: Callable, dictionary: dict):
        """Returns a filtered dictionary of values that pass the check."""
        return {k: v for k, v in dictionary.items() if check(v)}

    @staticmethod
    def match_mixed(variant_one: str, variant_two: str):
        """Matches and returns a single output from two"""
        return variant_one or variant_two

    @staticmethod
    def interaction_from_type(
        data,
    ) -> Optional[
        Union[
            ApplicationCommandInteraction,
            ButtonInteraction,
            SelectMenuInteraction,
            AutoCompleteInteraction,
            ModalSubmitInteraction,
        ]
    ]:
        interaction_types = {
            2: ApplicationCommandInteraction,
            3: lambda client, data: SelectMenuInteraction(client, data)
            if data["data"].get("values")
            else ButtonInteraction(client, data),
            4: AutoCompleteInteraction,
            5: ModalSubmitInteraction,
        }

        interaction_type = data["type"]
        interaction_cls = interaction_types.get(interaction_type)

        if not interaction_cls:
            logger.warning(f"Unknown interaction type: {interaction_type}")
            return None

        return interaction_cls(self.client, data)  # type: ignore

    def channel_from_type(self, channel_data: discord_typings.ChannelData):
        channel_type = channel_data["type"]

        if channel_cls := self.channels_types.get(channel_type):
            return channel_cls(self.client, channel_data)

        raise InvalidArgumentType(f"Unknown channel type: {channel_type}")

    @staticmethod
    def compute_timedelta(dt: datetime.datetime):
        if dt.tzinfo is None:
            dt = dt.astimezone()
        now = datetime.datetime.now(datetime.timezone.utc)
        return max((dt - now).total_seconds(), 0)

    async def sleep_until(
        self, when: Union[datetime.datetime, int, float], result: Optional[T] = None
    ) -> Optional[T]:
        if when == datetime.datetime:
            delta = self.compute_timedelta(when)  # type: ignore

        return await asyncio.sleep(delta if when == datetime.datetime else when, result)

    def remove_markdown(self, text: str, *, ignore_links: bool = True) -> str:
        def replacement(match):
            groupdict = match.groupdict()
            return groupdict.get("url", "")

        regex = self._MARKDOWN_STOCK_REGEX
        if ignore_links:
            regex = f"(?:{self._URL_REGEX}|{regex})"
        return re.sub(regex, replacement, text, 0, re.MULTILINE)

    def escape_markdown(
        self, text: str, *, as_needed: bool = False, ignore_links: bool = True
    ) -> str:
        if as_needed:
            text = re.sub(r"\\", r"\\\\", text)
            return self._MARKDOWN_ESCAPE_REGEX.sub(r"\\\1", text)

        def replacement(match):
            grouping = match.groupdict()

            if is_url := grouping.get("url"):
                return is_url

            return "\\" + grouping["markdown"]

        regex = self._MARKDOWN_STOCK_REGEX
        if ignore_links:
            regex = f"(?:{self._URL_REGEX}|{regex})"

        return re.sub(regex, replacement, text, 0, re.MULTILINE)

    @staticmethod
    def escape_mentions(text: str) -> str:
        return re.sub(r"@(everyone|here|[!&]?\d{17,20})", "@\u200b\\1", text)

    @staticmethod
    def utcnow() -> datetime.datetime:
        return datetime.datetime.now(datetime.timezone.utc)

    @staticmethod
    def cancel_tasks(loop) -> None:
        tasks = {t for t in asyncio.all_tasks(loop=loop) if not t.done()}

        if not tasks:
            return

        for task in tasks:
            task.cancel()
        logger.debug(f"Cancelled {len(tasks)} tasks")
        loop.run_until_complete(asyncio.gather(*tasks, return_exceptions=True))

    @staticmethod
    def cleanup_loop(loop) -> None:
        try:
            Utils.cancel_tasks(loop)
            logger.debug("Shutting down async generators.")
            loop.run_until_complete(loop.shutdown_asyncgens())
        finally:
            loop.close()

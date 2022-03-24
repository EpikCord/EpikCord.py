import asyncio
import re
import datetime
from typing import Union, Optional, TypeVar
from .thread import *
from .channel import *

T = TypeVar('T')
class Utils:
    """
    A utility class, used to make difficult things easy.

    Attributes:
    ----------
    client: Client
        The client that this utility class is attached to.
        
    """

    def __init__(self, client):
        self.client = client
        self. _MARKDOWN_ESCAPE_SUBREGEX = '|'.join(
            r'\{0}(?=([\s\S]*((?<!\{0})\{0})))'.format(c) for c in ('*', '`', '_', '~', '|'))

        self._MARKDOWN_ESCAPE_COMMON = r'^>(?:>>)?\s|\[.+\]\(.+\)'

        self._MARKDOWN_ESCAPE_REGEX = re.compile(
            fr'(?P<markdown>{self._MARKDOWN_ESCAPE_SUBREGEX}|{self._MARKDOWN_ESCAPE_COMMON})', re.MULTILINE)

        self._URL_REGEX = r'(?P<url><[^: >]+:\/[^ >]+>|(?:https?|steam):\/\/[^\s<]+[^<.,:;\"\'\]\s])'

        self._MARKDOWN_STOCK_REGEX = fr'(?P<markdown>[_\\~|\*`]|{self._MARKDOWN_ESCAPE_COMMON})'


    def channel_from_type(self, channel_data: dict):
        channel_type = channel_data.get("type")
        if channel_type == 0:
            return GuildTextChannel(self.client, channel_data)
        elif channel_type == 1:
            return DMChannel(self.client, channel_data)
        elif channel_type == 2:
            return VoiceChannel(self.client, channel_data)
        elif channel_type == 4:
            return ChannelCategory(self.client, channel_data)
        elif channel_type == 5:
            return GuildNewsChannel(self.client, channel_data)
        elif channel_type == 6:
            return GuildStoreChannel(self.client, channel_data)
        elif channel_type == 10:
            return GuildNewsThread(self.client, channel_data)
        elif channel_type == 11:
            return Thread(self.client, channel_data)
        elif channel_type == 12:
            return PrivateThread(self.client, channel_data)
        elif channel_type == 13:
            return GuildStageChannel(self.client, channel_data)

    def compute_timedelta(self, dt: datetime.datetime):
        if dt.tzinfo is None:
            dt = dt.astimezone()
        now = datetime.datetime.now(datetime.timezone.utc)
        return max((dt - now).total_seconds(), 0)


    async def sleep_until(self, when: Union[datetime.datetime, int, float], result: Optional[T] = None) -> Optional[T]:
        if when == datetime.datetime:
            delta = self.compute_timedelta(when)

        return await asyncio.sleep(delta if when == datetime.datetime else when, result)


    def remove_markdown(self, text: str, *, ignore_links: bool = True) -> str:
        def replacement(match):
            groupdict = match.groupdict()
            return groupdict.get('url', '')

        regex = self._MARKDOWN_STOCK_REGEX
        if ignore_links:
            regex = f'(?:{self._URL_REGEX}|{regex})'
        return re.sub(regex, replacement, text, 0, re.MULTILINE)


    def escape_markdown(self, text: str, *, as_needed: bool = False, ignore_links: bool = True) -> str:
        if not as_needed:

            def replacement(match):
                groupdict = match.groupdict()
                if is_url := groupdict.get('url'):
                    return is_url
                return '\\' + groupdict['markdown']

            regex = self._MARKDOWN_STOCK_REGEX
            if ignore_links:
                regex = f'(?:{self._URL_REGEX}|{regex})'
            return re.sub(regex, replacement, text, 0, re.MULTILINE)
        else:
            text = re.sub(r'\\', r'\\\\', text)
            return self._MARKDOWN_ESCAPE_REGEX.sub(r'\\\1', text)


    def escape_mentions(self, text: str) -> str:
        return re.sub(r'@(everyone|here|[!&]?[0-9]{17,20})', '@\u200b\\1', text)


    def utcnow(self) -> datetime.datetime:
        return datetime.datetime.now(datetime.timezone.utc)

    def cancel_tasks(self, loop) -> None:
        tasks = {t for t in asyncio.all_tasks(loop=loop) if not t.done()}

        if not tasks:
            return

        for task in tasks:
            task.cancel()
        logger.debug(f"Cancelled {len(tasks)} tasks")
        loop.run_until_complete(asyncio.gather(*tasks, return_exceptions=True))


    def cleanup_loop(self, loop) -> None:
        try:
            self.cancel_tasks(loop)
            logger.debug("Shutting down async generators.")
            loop.run_until_complete(loop.shutdown_asyncgens())
        finally:
            loop.close()

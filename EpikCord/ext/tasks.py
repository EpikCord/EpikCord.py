import asyncio
import typing
from datetime import timedelta

from ..utils import Coroutine


class Task:
    def __init__(self, wrapped_func: Coroutine, duration: float, max_runs: int):
        self.wrapped_func: Coroutine = wrapped_func
        self.duration: float = duration
        self.max_runs: int = max_runs
        self.runs: int = 0

    async def start(self, *args: typing.Any, **kwargs: typing.Any):
        while self.runs < self.max_runs:
            await self.wrapped_func(*args, **kwargs)

            if self.max_runs > 0:
                self.runs += 1

            await asyncio.sleep(self.duration)

    def run(self, *args: typing.Any, **kwargs: typing.Any):
        return asyncio.create_task(self.start(*args, **kwargs))


def task(duration: timedelta, max_runs=-1):
    def wrap(function):
        return Task(function, duration.total_seconds(), max_runs)

    return wrap

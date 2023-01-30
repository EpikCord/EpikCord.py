import asyncio
import typing
from datetime import timedelta
from typing import Callable, Coroutine


class Task:
    def __init__(
        self,
        wrapped_func: Callable[..., Coroutine],
        duration: float,
        max_runs: int,
    ):
        self.wrapped_func: Callable[..., Coroutine] = wrapped_func
        self.duration: float = duration
        self.max_runs: int = max_runs
        self.runs: int = 0
        self._task: typing.Optional[asyncio.Task] = None

    async def start(self, *args: typing.Any, **kwargs: typing.Any):
        while self.runs < self.max_runs:
            await self.wrapped_func(*args, **kwargs)

            if self.max_runs > 0:
                self.runs += 1

            await asyncio.sleep(self.duration)

    def run(self, *args: typing.Any, **kwargs: typing.Any):
        self._task = asyncio.create_task(self.start(*args, **kwargs))

    def cancel(self):
        if self._task is not None:
            self._task.cancel()


def task(duration: timedelta, max_runs=-1):
    def wrap(function):
        return Task(function, duration.total_seconds(), max_runs)

    return wrap

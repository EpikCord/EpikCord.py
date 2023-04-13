import asyncio
import typing
from datetime import timedelta
from logging import getLogger
from typing import Callable, Coroutine, Final

INFINITE_RUNS: Final[int] = -1

logger = getLogger("EpikCord.tasks")


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
        self.runs_count: int = INFINITE_RUNS
        self._task: typing.Optional[asyncio.Task] = None

    async def start(self, *args: typing.Any, **kwargs: typing.Any):
        logger.info(f"Starting task {self.wrapped_func.__name__}")

        while (
            self.runs_count < self.max_runs if self.has_limited_runs else True
        ):
            await self.wrapped_func(*args, **kwargs)

            self.runs_count += 1

            await asyncio.sleep(self.duration)

            logger.debug(
                f"Ran task {self.wrapped_func.__name__} for "
                f"{self.runs_count} time(s)."
            )

    @property
    def has_limited_runs(self) -> bool:
        return self.max_runs != INFINITE_RUNS

    def run(self, *args: typing.Any, **kwargs: typing.Any):
        self._task = asyncio.create_task(self.start(*args, **kwargs))
        self._task.set_name(self.wrapped_func.__name__)
        self._task.add_done_callback(
            lambda task: logger.info(f"Task {task.get_name()} finished.")
        )

    def cancel(self):
        logger.info(f"Cancelling task {self.wrapped_func.__name__}")
        if self._task is not None:
            self._task.cancel()


def task(duration: timedelta, max_runs=INFINITE_RUNS):
    def wrap(function):
        return Task(function, duration.total_seconds(), max_runs)

    return wrap

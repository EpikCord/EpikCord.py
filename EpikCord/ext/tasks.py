import datetime
from typing import Callable, Optional
from time import time as _time
import asyncio
from ..exceptions import TaskFailedError

_EPOCH = datetime.datetime(1970, 1, 1)


class TimeParser:
    @staticmethod
    def get_time_since_epoch(
        year: int = 0,
        month: int = 0,
        day: int = 0,
        hour: int = 0,
        minute: int = 0,
        seconds: float = 0,
    ) -> float:
        date = datetime.datetime(year, month, day, hour, minute, seconds)

        delta = date - _EPOCH
        return delta.total_seconds()

    @staticmethod
    def total_seconds(
        year: int = 0,
        month: int = 0,
        day: int = 0,
        hour: int = 0,
        minute: int = 0,
        seconds: float = 0,
    ) -> float:
        month += year * 365
        day += month * 30
        hour += day * 24
        minute += hour * 60
        seconds += minute * 60
        return seconds


class Tasks:
    def __init__(self, client) -> None:
        self.client = client

    def add_task(
        self,
        task: Callable[..., None],
        interval: Optional[int] = None,
        start: Optional[float] = None,
        until: Optional[float] = None,
        **kwargs,
    ):
        """Adds a background task (Tasks that run silently in the background)

        This task can be used to monitor the bot's performance, change and send stuff routinely
        through webhooks, etc
        You can set the time of when it starts, stops and  add which arguments to give to the task
        You may also define whether to run once or run indefinitely

        Args:
            task (Callable): The function to run on the background
            interval (Optional[int]): The interval (in seconds) for a delay between when the instance of the task stops and starts again.Defaults to 5.
            You may use `TimeParser.total_seconds` method
            instances (Optional[int]): The number of instances to start after delay. Usually unlimited
            start (Optional[float]): The time to start, you may use `TimeParser.get_time_since_epoch` method to give the seconds since python epoch to this arg
            until (optional[float]): The time to end, you may use `TimeParser.get_time_since_epoch` method to give the seconds since python epoch to this arg


        """
        kwargs["interval"] = interval
        kwargs["start"] = start
        kwargs["until"] = until

        async def full_task(client, task, **kwargs):
            async def task_func(client, interval):
                try:
                    await task(client)
                except Exception as e:
                    raise TaskFailedError(f"Task failed due to: {e}")

                await asyncio.sleep(interval)

            interval = int(kwargs.get("interval", 5))
            task_start = False
            nb_instances = kwargs.get("instances")
            if kwargs.get("start") and kwargs.get("until"):  # Start when and do until
                current_time = _time()
                until = float(kwargs.get("until"))
                if current_time >= float(kwargs.get("start")) or task_start:
                    while current_time >= until:
                        await task_func(client, interval)

            elif nb_instances:
                instances = int(nb_instances)
                finished_instances = 0
                while instances > finished_instances:
                    await task_func(client, interval)

            else:
                await task_func(client, interval)

        task = asyncio.get_event_loop().create_task(
            full_task(self.client, task, **kwargs)
        )
        self.client.task.append(task)
        return task

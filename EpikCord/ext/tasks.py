import datetime
from typing import Callable, Optional
import asyncio
from ..exceptions import TaskFailedError

_EPOCH = datetime.datetime(1970, 1, 1)
__all__ = (
    "TimeParser",
    "Tasks",
)




@staticmethod
def total_seconds(
    day: int = 0,
    hour: int = 0,
    minute: int = 0,
    seconds: float = 0,
) -> float:
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
        **kwargs,
    ):
        """Adds a background task (Tasks that run silently in the background)

        This task can be used to monitor the bot's performance, change and send stuff routinely
        through webhooks, etc
        You can set the time of when it starts, stops and  add which arguments to give to the task
        You may also define whether to run once or run indefinitely

        Args:
            task (Callable): 
            The function to run on the background
            interval (Optional[int]): 
            The interval (in seconds) for a delay between when the instance of the task stops and starts again.Defaults to 5.
            You may use `TimeParser.total_seconds` method
            instances (Optional[int]): 
            The number of instances to start after delay. Usually unlimited

        """
        kwargs["interval"] = interval

        async def full_task(client, task, **kwargs):
            async def task_func(interval):
                try:
                    await task(client)
                except Exception as e:
                    raise TaskFailedError(f"Task failed due to: {e}")

                await asyncio.sleep(interval)

            interval = interval if interval <= 0 else 5
            task_start = False
            nb_instances = kwargs.get("limit")

            if nb_instances:
                instances = int(nb_instances)
                finished_instances = 0
                while instances > finished_instances:
                    await task_func(client, interval)

            else:
                await task_func(client, interval)

        task = asyncio.get_event_loop().create_task(
            full_task(self.client, task, **kwargs)
        )
        self.client.tasks.append(task)
        return task

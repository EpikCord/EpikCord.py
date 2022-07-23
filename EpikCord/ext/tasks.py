import asyncio
import typing

# time constants in seconds
MINUTE = 60
HOUR   = MINUTE * 60
DAY    = HOUR   * 24
WEEK   = DAY    * 7

class Task:
    def __init__(self, wrapped_func, duration: int, max_runs: int):
        self.wrapped_func = wrapped_func
        self.duration = duration
        self.max_runs = max_runs
        self.runs = 0
    

    async def start(self, *args: typing.Any, **kwargs: typing.Any):
        if self.max_runs <= 0:
            cond = lambda: True
        else:
            cond = lambda: self.runs < self.max_runs
        

        while cond():
            await self.wrapped_func(*args, **kwargs)
            self.runs += 1
            await asyncio.sleep(self.duration)

    def run(self, *args: typing.Any, **kwargs: typing.Any):
        return asyncio.create_task(self.start(*args, **kwargs))


def task(seconds = 0, minutes = 0, hours = 0, days = 0, weeks = 0, max_runs = -1):
    duration = seconds
    duration += minutes * MINUTE
    duration += hours * HOUR
    duration += days  * DAY
    duration += weeks * WEEK
    
    def wrap(function):
        return Task(function, duration, max_runs)
    return wrap
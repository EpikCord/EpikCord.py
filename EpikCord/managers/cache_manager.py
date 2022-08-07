import asyncio
from typing import Any, Optional


class CacheManager:
    def __init__(self, limit= 1000):
        self.limit = limit
        self.cache = {}
        asyncio.create_task(self.limit_check())


    async def limit_check(self):
        while True:
            if len(self.cache) >= self.limit:
                self.cache.pop(next(iter(self.cache)))

    def add_to_cache(self, key, value):
        self.cache[key] = value

    def remove_from_cache(self, key):
        self.cache.pop(key, None)

    def get(self, key, default: Optional[Any] = None) -> Any:
        return self.cache.get(key, default)

    def is_in_cache(self, key):
        return key in self.cache

    def clear_cache(self):
        self.cache = {}

    def __dict__(self):
        return self.cache

    def __str__(self):
        return f"<CacheManager cache={self.cache}>"

    def __int__(self):
        return len(self.cache)

    def __len__(self):
        return len(self.cache)

    def __repr__(self):
        return self.__str__()

    def __getitem__(self, key):
        return self.cache[key]

    def __setitem__(self, key, value):
        self.cache[key] = value

    def __delitem__(self, key):
        self.cache.pop(key, None)

    def __contains__(self, key):
        return key in self.cache

    def __iter__(self):
        return iter(self.cache)

    def __next__(self):
        return next(self.cache)

    def __eq__(self, other):
        return self.cache == other.cache

    def __ne__(self, other):
        return self.cache != other.cache

    def __gt__(self, other):
        return self.cache > other.cache

    def __ge__(self, other):
        return self.cache >= other.cache

    def __lt__(self, other):
        return self.cache < other.cache

    def __le__(self, other):
        return self.cache <= other.cache

    def __hash__(self):
        return hash(self.cache)

    def __call__(self):
        return self.cache


# This is the base cache manager, people can extend this to make their own cache managers

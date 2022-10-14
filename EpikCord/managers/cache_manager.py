from __future__ import annotations

from typing import Any, Dict, Iterator, Optional, Union


class CacheManager:
    def __init__(self):
        self.cache: Dict[Any, Any] = {}

    def add_to_cache(self, key: Union[int, str], value: Any):
        self.cache[key] = value

    def remove_from_cache(self, key):
        self.cache.pop(key, None)

    def get(self, key, default: Optional[Any] = None) -> Any:
        return self.cache.get(key, default)

    def is_in_cache(self, key: str):
        return key in self.cache

    def clear_cache(self):
        self.cache = {}

    def __dict__(self) -> Dict:  # type: ignore
        return self.cache

    def __str__(self) -> str:
        return f"<CacheManager cache={self.cache}>"

    def __int__(self) -> int:
        return len(self.cache)

    def __len__(self) -> int:
        return len(self.cache)

    def __repr__(self) -> str:
        return self.__str__()

    def __getitem__(self, key: str) -> Any:
        return self.cache[key]

    def __setitem__(self, key: str, value: Any) -> Any:
        self.cache[key] = value

    def __delitem__(self, key: str) -> None:
        self.cache.pop(key, None)

    def __contains__(self, key: str) -> bool:
        return key in self.cache

    def __iter__(self) -> Iterator:
        return iter(self.cache)

    def __eq__(self, other: CacheManager) -> bool:  # type: ignore
        return self.cache == other.cache

    def __ne__(self, other: CacheManager) -> bool:  # type: ignore
        return self.cache != other.cache

    def __gt__(self, other: CacheManager) -> bool:
        return len(self.cache) > len(other.cache)

    def __ge__(self, other: CacheManager) -> bool:
        return len(self.cache) >= len(other.cache)

    def __lt__(self, other: CacheManager) -> bool:
        return len(self.cache) < len(other.cache)

    def __le__(self, other: CacheManager) -> bool:
        return len(self.cache) <= len(other.cache)

    def __hash__(self) -> int:
        return hash(self.cache)

    def __call__(self) -> Dict:
        return self.cache


# !  This is the base cache manager, people can extend this to make their own cache managers

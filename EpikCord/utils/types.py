from typing import Callable, Coroutine as _Coroutine, Any

Coroutine = Callable[..., _Coroutine[Any, Any, Any]]
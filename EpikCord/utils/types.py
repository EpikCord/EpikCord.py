from typing import Any, Callable
from typing import Coroutine as _Coroutine

Coroutine = Callable[..., _Coroutine[Any, Any, Any]]

from typing import Any, Callable
from typing import Coroutine

AsyncFunction = Callable[..., Coroutine[Any, Any, Any]]

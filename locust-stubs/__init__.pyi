from typing import Any, Callable, Optional

class HttpUser:
    wait_time: Any
    def __init__(self, *args, **kwargs): ...

def task(weight: Optional[int] = None) -> Callable: ...

def between(min_wait: int, max_wait: int) -> Callable: ... 
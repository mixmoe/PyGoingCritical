import time
from functools import wraps
from typing import TypeVar

from .log import logger

_T = TypeVar("_T")


def TimeIt(func: _T) -> _T:
    assert callable(func)

    @wraps(func)
    def wrapper(*args, **kwargs):
        beginTime = time.time() * 1000
        try:
            return func(*args, **kwargs)
        finally:
            endTime = time.time() * 1000
            logger.debug(f"Function {func} cost {endTime-beginTime:.3f}ms")

    return wrapper  # type:ignore

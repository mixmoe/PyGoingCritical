import time
from functools import wraps
from typing import Callable

from .log import logger


def TimeIt(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        beginTime = time.time() * 1000
        try:
            return func(*args, **kwargs)
        except Exception:
            endTime = time.time() * 1000
            logger.debug(f"Function {func} cost {endTime-beginTime:.3f}ms")

    return wrapper


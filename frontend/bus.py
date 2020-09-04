from concurrent.futures.thread import ThreadPoolExecutor
from functools import partial, wraps
from time import sleep
from typing import Callable, Dict, Optional, Set, Tuple

from utils.log import logger
from utils.misc import TimeIt

Handler_T = Callable[..., None]


class EventBus:
    _events: Dict[str, Set[Handler_T]] = {}
    _executor = ThreadPoolExecutor()

    @classmethod
    def subscribe(cls, name: str, handler: Optional[Handler_T] = None) -> Handler_T:
        if handler is None:
            return partial(cls.subscribe, name)  # type:ignore

        @TimeIt
        @wraps(handler)
        def wrapper(*args, **kwargs):
            try:
                return handler(*args, **kwargs)
            except Exception:
                logger.exception(
                    f"Error occurred in function {handler!r} "
                    f"during handling event {name!r}"
                )

        handlers: Set[Handler_T] = cls._events.get(name, set())
        handlers.add(wrapper)
        cls._events[name] = handlers

        logger.debug(
            f"Function {handler!r} has been successful registered "
            f"as a handler of event {name!r}"
        )

        return wrapper

    @classmethod
    @TimeIt
    def broadcast(cls, name: str, *args, **kwargs) -> Tuple[int, int]:
        assert name in cls._events
        receivers = cls._events[name]
        futures = [
            *map(lambda x: cls._executor.submit(lambda: x(*args, **kwargs)), receivers)
        ]
        while [*filter(lambda x: not x.done(), futures)]:
            sleep(0.1)
        error, total = (
            len([*filter(lambda x: x.exception(), futures)]),
            len(futures),
        )
        logger.debug(
            f"Event {name!r} broadcast finished, "
            f"{error} handlers failed in total {total}."
        )
        return error, total

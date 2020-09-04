from functools import partial, wraps
from typing import Callable, Dict, Optional, Set, Tuple, Union

from utils.log import logger
from utils.misc import TimeIt

Handler_T = Callable[..., None]


class EventBus:
    _events: Dict[str, Set[Handler_T]] = {}

    @classmethod
    def subscribe(
        cls, name: str, handler: Optional[Handler_T] = None
    ) -> Union[Handler_T, Callable[..., Handler_T]]:
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
                raise

        handlers: Set[Handler_T] = cls._events.get(name, set())
        handlers.add(wrapper)
        cls._events[name] = handlers

        logger.debug(
            f"Function {handler!r} has been successful registered "
            f"as a handler of event {name!r}"
        )

        return handler

    @classmethod
    @TimeIt
    def broadcast(cls, name: str, *args, **kwargs) -> Tuple[int, int]:
        subscribers: Set[Handler_T] = cls._events.get(name, set())
        error, total = 0, len(subscribers)
        for subscriber in subscribers:
            try:
                subscriber(*args, **kwargs)
            except Exception:
                error += 1
        logger.debug(
            f"Event {name!r} broadcast finished, "
            f"{error} handlers failed in total {total}."
        )
        return error, total

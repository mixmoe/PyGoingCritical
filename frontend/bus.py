from functools import partial, wraps
from typing import Any, Callable, Dict, Optional, Set, Tuple, overload

from utils.log import logger
from utils.misc import TimeIt

Handler_T = Callable[..., None]


class _EventBus:
    def __init__(self, name: str) -> None:
        self.name = name
        self.events: Dict[str, Set[Handler_T]] = {}

    @overload
    def subscribe(self, event: str) -> Callable[[Handler_T], Handler_T]:
        ...

    @overload
    def subscribe(self, event: str, handler: Handler_T) -> Handler_T:
        ...

    def subscribe(self, event: str, handler: Optional[Handler_T] = None):
        if handler is None:
            return partial(self.subscribe, event)

        @TimeIt
        @wraps(handler)
        def wrapper(*args, **kwargs):
            try:
                return handler(*args, **kwargs)
            except Exception:
                logger.exception(
                    f"Error occurred in function {handler!r} "
                    f"during handling event {self.name}>{event!r}"
                )
                raise

        self.events[event] = self.events.get(event, set()) | {wrapper}  # type:ignore
        return handler

    @TimeIt
    def broadcast(self, event: str, *args, **kwargs) -> Tuple[int, int]:
        subscribers: Set[Handler_T] = self.events.get(event, set())
        errors, total = 0, len(subscribers)
        for subscriber in subscribers:
            try:
                subscriber(*args, **kwargs)
            except Exception:
                errors += 1
        logger.info(
            f"Event {self.name}>{event!r} broadcast finished, "
            f"{errors} handlers failed in total {total}."
        )
        return errors, total


class EventBusNamespace:
    _eventBuses: Dict[str, _EventBus] = {}
    _eventProperty: Dict[str, Dict[str, Any]] = {}

    @classmethod
    def register(cls, name: str) -> _EventBus:
        cls._eventBuses[name] = _EventBus(name)
        return cls.get(name)

    @classmethod
    @overload
    def get(cls, name: str, *, create: bool = False) -> _EventBus:
        ...

    @classmethod
    @overload
    def get(cls, name: str, property: str) -> Any:
        ...

    @classmethod
    def get(cls, name: str, property: Optional[str] = None, *, create: bool = False):
        if (name not in cls._eventBuses) and create:
            cls.register(name)
        return (
            cls._eventBuses[name]
            if property is None
            else cls._eventProperty[name][property]
        )

    @classmethod
    def set(cls, name: str, **property) -> Dict[str, Any]:
        assert name in cls._eventBuses
        cls._eventProperty[name] = {**cls._eventProperty.get(name, {}), **property}
        return cls._eventProperty[name]


EventBus = EventBusNamespace.get("default")

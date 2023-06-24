from typing import Callable, Dict

from http import HTTPMethod

_handlers: Dict[HTTPMethod, Dict[str, Callable]] = {}


def register(method: HTTPMethod, path: str) -> Callable[[Callable], Callable[[], str]]:
    def _inner(handler: Callable[[], str]) -> Callable[[], str]:
        _handlers[method][path] = handler
        return handler
    return _inner

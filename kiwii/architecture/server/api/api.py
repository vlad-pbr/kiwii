import re

from typing import Callable, Dict, Tuple, Optional
from http import HTTPMethod, HTTPStatus

_handlers: Dict[str, Dict[str, Callable[[Tuple], Tuple[HTTPStatus, str]]]] = {}


def register(method: HTTPMethod, path: str) -> Callable[[Callable], Callable[[Tuple], Tuple[HTTPStatus, str]]]:
    strmethod = str(method)

    def _inner(handler: Callable[[], Tuple[HTTPStatus, str]]) -> Callable[[Tuple], Tuple[HTTPStatus, str]]:
        if strmethod not in _handlers:
            _handlers[strmethod]: Dict[str, Callable[[Tuple], Tuple[HTTPStatus, str]]] = {}
        _handlers[strmethod][path] = handler
        return handler
    return _inner


def handle(method: str, path: str) -> Tuple[HTTPStatus, Optional[str]]:

    if method not in _handlers:
        return HTTPStatus.NOT_FOUND, None

    for path_pattern, handler in _handlers[method].items():
        match = re.match(path_pattern, path)
        if match:
            return handler(match.groups())

    return HTTPStatus.NOT_FOUND, None

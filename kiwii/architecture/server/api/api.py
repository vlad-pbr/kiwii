import re

from typing import Callable, Dict, Tuple
from http import HTTPMethod, HTTPStatus

from kiwii.architecture.server.shared.models import Request, Response

_handlers: Dict[HTTPMethod, Dict[str, Callable[[Tuple], Response]]] = {}


def register(method: HTTPMethod, path: str) -> Callable[[Callable], Callable[[Tuple], Response]]:
    def _inner(handler: Callable[[Tuple], Response]) -> Callable[[Tuple], Response]:
        if method not in _handlers:
            _handlers[method]: Dict[str, Callable[[Tuple], Response]] = {}
        _handlers[method][path] = handler
        return handler
    return _inner


def handle(request: Request) -> Response:

    if request.method not in _handlers:
        return Response(status=HTTPStatus.NOT_FOUND)

    for path_pattern, handler in _handlers[request.method].items():
        match = re.match(path_pattern, request.path)
        if match:
            return handler(match.groups())

    return Response(status=HTTPStatus.NOT_FOUND)

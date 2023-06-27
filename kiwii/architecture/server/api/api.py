import re
from http import HTTPStatus, HTTPMethod
from re import Match
from typing import Dict, Callable, Optional

from kiwii.architecture.server.api.auth import disable_authentication, authenticate_request, authenticate_user
from kiwii.architecture.server.api.shared.types import RouteHandler
from kiwii.architecture.server.shared.models import Request, Response, Route
from kiwii.shared.logging_utils import get_critical_exit_logger, LoggerName

_handlers: Dict[Route, RouteHandler] = {}
_logger = get_critical_exit_logger(LoggerName.API)


def initialize(log_level: str) -> None:

    # apply log level
    _logger.setLevel(log_level)

    # register routes
    import kiwii.architecture.server.api.routes
    _ = kiwii.architecture.server.api.routes


def register(method: HTTPMethod,
             path_regex: str,
             authenticate: bool = True) -> Callable[[RouteHandler], RouteHandler]:
    def _inner(handler: RouteHandler) -> RouteHandler:

        # validate path regex and create compiled pattern
        try:
            pattern = re.compile(path_regex)
        except re.error as e:
            _logger.error(f"disabling route '{path_regex}' as it is an invalid regex: {e}")
            return handler

        # build route object
        route = Route(method=method, pattern=pattern)

        # add handler
        _handlers[route] = handler

        # opt out of authentication if specified
        if not authenticate:
            disable_authentication(route)

        _logger.info(f"registered route: '{path_regex}'")

        return handler

    return _inner


def handle(request: Request) -> Response:

    # find matching route
    route: Optional[Route] = None
    handler: Optional[RouteHandler] = None
    match: Optional[Match[str]] = None
    for _route, _handler in _handlers.items():
        if _route.method == request.endpoint.method:
            _match = _route.pattern.match(request.endpoint.path)
            if _match:
                route = _route
                handler = _handler
                match = _match
                break

    # if matching route was found and user is authenticated for the matching route - handle
    if route:
        if authenticate_request(route, request):
            return handler(match.groups())

    # if matching route was not found, but user is authenticated - report "Not Found"
    else:
        if authenticate_user(request.headers):
            return Response(status=HTTPStatus.NOT_FOUND)

    return Response(status=HTTPStatus.UNAUTHORIZED)

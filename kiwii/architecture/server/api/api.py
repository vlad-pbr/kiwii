import re
from http import HTTPStatus
from typing import Dict, Callable

from kiwii.architecture.server.api.auth import disable_authentication, authenticate_request
from kiwii.architecture.server.api.shared.types import EndpointHandler
from kiwii.architecture.server.shared.models import Request, Response, Route
from kiwii.shared.logging_utils import get_critical_exit_logger, LoggerName

_handlers: Dict[Route, EndpointHandler] = {}
_logger = get_critical_exit_logger(LoggerName.API)


def initialize(log_level: str) -> None:

    # apply log level
    _logger.setLevel(log_level)

    # register endpoints
    import kiwii.architecture.server.api.endpoints
    _ = kiwii.architecture.server.api.endpoints


def register(route: Route,
             authenticate: bool = True) -> Callable[[EndpointHandler], EndpointHandler]:
    def _inner(handler: EndpointHandler) -> EndpointHandler:

        # validate path regex
        try:
            re.compile(route.path)
        except re.error as e:
            _logger.error(f"disabling endpoint '{route.path}' as it is an invalid regex: {e}")
            return handler

        # add handler
        _handlers[route] = handler

        # opt out of authentication if specified
        if not authenticate:
            disable_authentication(route)

        _logger.info(f"registered endpoint: '{route.path}'")

        return handler
    return _inner


def handle(request: Request) -> Response:

    # make sure authentication checks out
    if not authenticate_request(request):
        return Response(status=HTTPStatus.FORBIDDEN)

    # find matching handler
    for route, handler in _handlers.items():
        match = re.match(route.path, request.route.path)
        if match:
            return handler(match.groups())

    # no handler for provided request
    return Response(status=HTTPStatus.NOT_FOUND)

import re
from http import HTTPStatus, HTTPMethod
from typing import Dict

from kiwii.architecture.server.api.shared.models import RouteParams
from kiwii.architecture.server.api.shared.types import RouteHandler, RouteDecorator
from kiwii.architecture.server.shared.models import Request, Response, Route
from kiwii.shared.logging_utils import get_critical_exit_logger, LoggerName

_handlers: Dict[Route, RouteHandler] = {}
_logger = get_critical_exit_logger(LoggerName.API)


def initialize(log_level: str, expose_doc: bool) -> None:

    # apply log level
    _logger.setLevel(log_level)

    # register core routes
    import kiwii.architecture.server.api.routes.core
    _ = kiwii.architecture.server.api.routes.core

    # register optional routes if required
    if expose_doc:
        import kiwii.architecture.server.api.routes.optional.doc
        _ = kiwii.architecture.server.api.routes.optional.doc


def register(method: HTTPMethod,
             path_regex: str) -> RouteDecorator:
    def _inner(handler: RouteHandler) -> RouteHandler:

        # validate path regex and create compiled pattern
        try:
            pattern = re.compile(path_regex)
        except re.error as e:
            _logger.error(f"disabling route '{path_regex}' as it is an invalid regex: {e}")
            return handler

        # build route object and add handler
        route = Route(method=method, pattern=pattern)
        _handlers[route] = handler
        _logger.debug(f"registered route: '{path_regex}'")

        return handler

    return _inner


def handle(request: Request) -> Response:

    # find and use matching route
    for _route, _handler in _handlers.items():
        if _route.method == request.endpoint.method:
            _match = _route.pattern.match(request.endpoint.path)
            if _match:
                _logger.debug(f"request for '{request.endpoint.path}' handled by route '{_route.pattern.pattern}'")
                return _handler(
                    RouteParams(
                        request=request,
                        path_params=_match.groups()
                    )
                )

    return Response(status=HTTPStatus.NOT_FOUND)

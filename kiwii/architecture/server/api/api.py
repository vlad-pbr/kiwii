"""
Kiwii API static class. Not actually a class as static classes are not pythonic.
"""

from http import HTTPStatus
from typing import Dict

from kiwii.architecture.server.api.shared.models import RouteParams
from kiwii.architecture.server.api.shared.types import RouteHandler, RouteDecorator
from kiwii.architecture.server.shared.models import Request, Response
from kiwii.architecture.shared.models import Route
from kiwii.shared.logging.logging import get_logger, ComponentLoggerName

handlers: Dict[Route, RouteHandler] = {}
logger = get_logger(ComponentLoggerName.API)


def initialize(log_level: str, expose_doc: bool) -> None:
    """Initializes API by registering requested routes and setting the requested log level."""

    # apply log level
    logger.setLevel(log_level)

    # register core routes
    import kiwii.architecture.server.api.routes.core
    _ = kiwii.architecture.server.api.routes.core

    # register optional routes if required
    if expose_doc:
        import kiwii.architecture.server.api.routes.optional.doc
        _ = kiwii.architecture.server.api.routes.optional.doc


def register(route: Route) -> RouteDecorator:
    """Decorator for the `Route` handlers which registers them with the API."""

    def _inner(handler: RouteHandler) -> RouteHandler:

        # register route-to-handler entity
        handlers[route] = handler
        logger.debug(f"registered route: '{route.pattern.pattern}'")

        return handler

    return _inner


def handle(request: Request) -> Response:
    """
    Client request handler method which is responsible for `Route` resolution and actual request handling
    by calling the matching `Route` handler.
    """

    # find matching route and handle the request
    for _route, _handler in handlers.items():
        if _route.method == request.endpoint.method:
            _match = _route.pattern.match(request.endpoint.path)
            if _match:
                logger.debug(f"request for '{request.endpoint.path}' handled by route '{_route.pattern.pattern}'")
                return _handler(
                    RouteParams(
                        request=request,
                        path_params=_route.params_type(*_match.groups())
                    )
                )

    return Response(status=HTTPStatus.NOT_FOUND)

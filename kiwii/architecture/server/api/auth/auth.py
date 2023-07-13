from functools import wraps
from http import HTTPStatus
from typing import Dict, Optional

from kiwii.architecture.server.api.auth.shared.models import AuthenticationHandlerParams
from kiwii.architecture.server.api.auth.shared.types import AuthenticationHandler, AuthenticationHandlerDecorator
from kiwii.architecture.server.api.shared.models import AuthenticationMethod, RouteParams
from kiwii.architecture.server.api.shared.types import RouteDecorator, RouteHandler
from kiwii.architecture.server.data.data import get_data_layer
from kiwii.architecture.server.shared.models import Response
from kiwii.architecture.shared.models.user_credentials import UserCredentials
from kiwii.data.data_structures.credentials import CredentialsDataStructure
from kiwii.shared.logging.componentloggername import ComponentLoggerName
from kiwii.shared.logging.logging import get_logger

authentication_handlers: Dict[AuthenticationMethod, AuthenticationHandler] = {}
logger = get_logger(ComponentLoggerName.API_AUTH)


def authenticate(method: AuthenticationMethod) -> RouteDecorator:
    """Decorator for the `Route` handlers which enforces a requested authentication method on decorated route."""

    def _inner(handler: RouteHandler) -> RouteHandler:
        @wraps(handler)
        def _handler(params: RouteParams) -> Response:

            # make sure requested authentication method has a handler
            authentication_handler: Optional[AuthenticationHandler] = authentication_handlers.get(method, None)
            if authentication_handler is None:
                logger.error(
                    f"endpoint '{params.request.endpoint}' is authenticated using authentication method '{method}' "
                    f"but an appropriate authentication method handler is not registered")

                return Response(status=HTTPStatus.INTERNAL_SERVER_ERROR)

            # perform authentication
            return authentication_handler(
                AuthenticationHandlerParams(
                    route_params=params,
                    route_handler=handler
                )
            )

        return _handler

    return _inner


def register(method: AuthenticationMethod) -> AuthenticationHandlerDecorator:
    """Decorator for authentication handlers to register with the authentication layer."""

    def _inner(handler: AuthenticationHandler) -> AuthenticationHandler:
        authentication_handlers[method] = handler
        logger.debug(f"registered authentication method handler: '{method}'")

        return handler

    return _inner


def initialize(credentials: Optional[UserCredentials], log_level: str) -> False:
    """
    Initialization entrypoint for authentication layer.

    Returns False if credentials were not provided and are also not present in persisted storage.
    Return True otherwise.
    """

    # set logging level
    logger.setLevel(log_level)

    # register authentication methods
    import kiwii.architecture.server.api.auth.authentication_methods
    _ = kiwii.architecture.server.api.auth.authentication_methods

    if credentials:
        get_data_layer().store(CredentialsDataStructure.from_literal(
            plaintext_credentials=credentials.as_authorization_basic()
        ))

        return True

    return get_data_layer().retrieve(CredentialsDataStructure) is not None

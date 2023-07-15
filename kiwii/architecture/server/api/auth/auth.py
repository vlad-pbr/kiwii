"""
Authentication and authorization static class.

Not actually a class as static classes are not pythonic.
"""

from functools import wraps
from http import HTTPStatus
from typing import Dict, Optional, List, Union

from kiwii.architecture.server.api.auth.consts import ADMIN_USER_ALLOWED_ROUTES
from kiwii.architecture.server.api.auth.shared.models import AuthenticationHandlerParams
from kiwii.architecture.server.api.auth.shared.types import AuthenticationHandler, AuthenticationHandlerDecorator
from kiwii.architecture.server.api.shared.models import AuthenticationMethod, RouteParams
from kiwii.architecture.server.api.shared.types import RouteDecorator, RouteHandler
from kiwii.architecture.server.data.data import get_data_layer
from kiwii.architecture.server.shared.models import Response, Endpoint
from kiwii.architecture.shared.models import Route
from kiwii.architecture.shared.models.user_credentials import UserCredentials
from kiwii.architecture.server.data.data_structures.credentials import CredentialsDataStructure
from kiwii.shared.logging.componentloggername import ComponentLoggerName
from kiwii.shared.logging.logging import get_logger

authentication_handlers: Dict[AuthenticationMethod, AuthenticationHandler] = {}
_authorization_acl: Dict[str, List[Union[Route, Endpoint]]] = {}
logger = get_logger(ComponentLoggerName.API_AUTH)


def authenticate(method: AuthenticationMethod) -> RouteDecorator:
    """Decorator for `Route` handlers which enforces a requested authentication method on decorated route."""

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


def add_permissions(credentials: CredentialsDataStructure, *endpoints: Union[Route, Endpoint]) -> None:
    """Allows user/agent authenticated with provided credentials to use provided routes."""

    if credentials.hash not in _authorization_acl:
        _authorization_acl[credentials.hash] = []

    _authorization_acl[credentials.hash].extend(endpoints)


def authorize(handler: RouteHandler) -> RouteHandler:
    """Decorator for `Route` handlers which enforces authorization on decorated route."""

    @wraps(handler)
    def _handler(params: RouteParams) -> Response:

        # make sure authentication handler has populated the authorization metadata
        if params.authorization is None:
            logger.error(
                f"endpoint '{params.request.endpoint}' is authorized, but authentication metadata was not populated")

            return Response(status=HTTPStatus.INTERNAL_SERVER_ERROR)

        # make sure ACL entry exists for given credentials and an associated route/endpoint exists in the ACL
        acl: Optional[List[Route]] = _authorization_acl.get(params.authorization.credentials.hash, None)
        if acl is None or params.route not in acl or not params.request.endpoint not in acl:
            return Response(status=HTTPStatus.UNAUTHORIZED)

        return handler(params)

    return _handler


def register(method: AuthenticationMethod) -> AuthenticationHandlerDecorator:
    """Decorator for authentication handlers to register with the authentication layer."""

    def _inner(handler: AuthenticationHandler) -> AuthenticationHandler:
        authentication_handlers[method] = handler
        logger.debug(f"registered authentication method handler: '{method}'")

        return handler

    return _inner


def initialize(admin_credentials: Optional[UserCredentials], log_level: str) -> False:
    """
    Initialization entrypoint for authentication + authorization layer.

    Returns False if credentials were not provided and are also not present in persisted storage.
    Return True otherwise.
    """

    # make sure that admin credentials were provided or already exist in persisted storage
    if admin_credentials:
        credentials_structure = CredentialsDataStructure.from_literal(
            plaintext_credentials=admin_credentials.as_authorization_basic()
        )
        get_data_layer().store(credentials_structure)
    else:
        credentials_structure = get_data_layer().retrieve(CredentialsDataStructure)
        if credentials_structure is None:
            return False

    # set logging level
    logger.setLevel(log_level)

    # add admin permissions to admin user
    add_permissions(credentials_structure, *ADMIN_USER_ALLOWED_ROUTES)

    # register authentication methods
    import kiwii.architecture.server.api.auth.authentication_methods
    _ = kiwii.architecture.server.api.auth.authentication_methods

    return True

from functools import wraps
from typing import Dict, Optional

from kiwii.architecture.server.api.auth.methods import handle_basic_auth
from kiwii.architecture.server.api.auth.shared.models import AuthenticationHandlerParams
from kiwii.architecture.server.api.auth.shared.types import AuthenticationHandler
from kiwii.architecture.server.api.shared.models import AuthenticationMethod, RouteParams
from kiwii.architecture.server.api.shared.types import RouteDecorator, RouteHandler
from kiwii.architecture.server.data.data import get_data_layer
from kiwii.architecture.server.shared.models import Response
from kiwii.architecture.shared.models.user_credentials import UserCredentials
from kiwii.data.data_structures.credentials import CredentialsDataStructure

METHOD_TO_HANDLER: Dict[AuthenticationMethod, AuthenticationHandler] = {
    AuthenticationMethod.BASIC: handle_basic_auth
}


def authenticate(method: AuthenticationMethod) -> RouteDecorator:
    """Decorator for the `Route` handlers which enforces a requested authentication method on decorated route."""

    def _inner(handler: RouteHandler) -> RouteHandler:

        @wraps(handler)
        def _handler(params: RouteParams) -> Response:
            return METHOD_TO_HANDLER[method](
                AuthenticationHandlerParams(
                    route_params=params,
                    route_handler=handler
                )
            )

        return _handler

    return _inner


def initialize(credentials: Optional[UserCredentials]) -> False:
    """
    Initialization entrypoint for authentication layer.

    Returns False if credentials were not provided and are also not present in persisted storage.
    Return True otherwise.
    """

    if credentials:
        get_data_layer().store(CredentialsDataStructure.from_literal(
            plaintext_credentials=credentials.as_authorization_basic()
        ))

        return True

    return get_data_layer().retrieve(CredentialsDataStructure) is not None

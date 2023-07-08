import base64
from functools import wraps
from typing import Dict, Optional

from kiwii.architecture.server.api.auth.shared.hash_utils import get_hash
from kiwii.architecture.server.api.auth.shared.models import AuthenticationHandlerParams
from kiwii.architecture.server.api.auth.shared.types import AuthenticationHandler
from kiwii.architecture.server.api.auth.methods import handle_basic_auth
from kiwii.architecture.server.api.shared.models import AuthenticationMethod, RouteParams
from kiwii.architecture.server.api.shared.models.user_credentials import UserCredentials
from kiwii.architecture.server.api.shared.types import RouteDecorator, RouteHandler
from kiwii.architecture.server.shared.models import Response
from kiwii.data.data import store
from kiwii.data.data_structures.user import AdminDataStructure

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
    """Initialization entrypoint for authentication layer."""

    if credentials:
        store(AdminDataStructure(
            credentials=get_hash(base64.b64encode(f"{credentials.username}:{credentials.password}".encode()).decode())
        ))

        return True

    else:

        # TODO read underlying storage if one is present

        return False

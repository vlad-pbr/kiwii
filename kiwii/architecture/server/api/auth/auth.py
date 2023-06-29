from typing import Dict

from kiwii.architecture.server.api.auth.shared.models import AuthenticationHandlerParams
from kiwii.architecture.server.api.auth.shared.types import AuthenticationHandler
from kiwii.architecture.server.api.auth.types import handle_basic_auth
from kiwii.architecture.server.api.shared.models import AuthenticationMethod
from kiwii.architecture.server.api.shared.types import RouteDecorator, RouteHandler

METHOD_TO_HANDLER: Dict[AuthenticationMethod, AuthenticationHandler] = {
    AuthenticationMethod.BASIC: handle_basic_auth
}


def authenticate(method: AuthenticationMethod) -> RouteDecorator:
    def _inner(handler: RouteHandler) -> RouteHandler:
        return METHOD_TO_HANDLER[method](
            AuthenticationHandlerParams(
                handler=handler
            )
        )

    return _inner

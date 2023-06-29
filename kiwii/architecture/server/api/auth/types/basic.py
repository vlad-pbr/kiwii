import re
import base64
from http import HTTPStatus
from functools import wraps

from kiwii.architecture.server.api.auth.shared.models import AuthenticationHandlerParams
from kiwii.architecture.server.api.shared.models import RouteParams
from kiwii.architecture.server.api.shared.types import RouteHandler
from kiwii.architecture.server.shared.models import Response

AUTHORIZATION_HEADER: str = "Authorization"
AUTHORIZATION_PATTERN: re.Pattern = re.compile(r"^Basic (.*)$")

# TODO delegate to actual storage
AUTHENTICATION_CREDENTIALS: str = base64.b64encode(b"admin:admin").decode()


def handle(auth_params: AuthenticationHandlerParams) -> RouteHandler:

    @wraps(auth_params.handler)
    def _inner(route_params: RouteParams) -> Response:

        # make sure authorization header is present
        authorization_header_value = route_params.request.headers.get(AUTHORIZATION_HEADER, "")
        if not authorization_header_value:
            return Response(status=HTTPStatus.UNAUTHORIZED)

        # make sure authorization value is valid
        authorization_value_match = AUTHORIZATION_PATTERN.match(authorization_header_value)
        if not authorization_value_match:
            return Response(status=HTTPStatus.UNAUTHORIZED)

        # make sure credentials match
        if authorization_value_match.groups()[0] != AUTHENTICATION_CREDENTIALS:
            return Response(status=HTTPStatus.UNAUTHORIZED)

        return auth_params.handler(route_params)

    return _inner

import base64
import re
from http import HTTPStatus

from kiwii.architecture.server.api.auth.shared.models import AuthenticationHandlerParams
from kiwii.architecture.server.api.shared.consts import HTTP_HEADER_AUTHORIZATION
from kiwii.architecture.server.shared.models import Response

AUTHORIZATION_PATTERN: re.Pattern = re.compile(r"^Basic (.*)$")

# TODO delegate to actual storage
AUTHENTICATION_CREDENTIALS: str = base64.b64encode(b"admin:admin").decode()


def handle(auth_params: AuthenticationHandlerParams) -> Response:
    """
    Performs `HTTP Basic Authorization`:
    - reads HTTP Authorization header
    - validates the value format
    - compares the credential value with actual credentials
    """

    # make sure authorization header is present
    authorization_header_value = auth_params.route_params.request.headers.get(HTTP_HEADER_AUTHORIZATION, "")
    if not authorization_header_value:
        return Response(status=HTTPStatus.UNAUTHORIZED)

    # make sure authorization value is valid
    authorization_value_match = AUTHORIZATION_PATTERN.match(authorization_header_value)
    if not authorization_value_match:
        return Response(status=HTTPStatus.UNAUTHORIZED)

    # make sure credentials match
    if authorization_value_match.groups()[0] != AUTHENTICATION_CREDENTIALS:
        return Response(status=HTTPStatus.UNAUTHORIZED)

    return auth_params.route_handler(auth_params.route_params)

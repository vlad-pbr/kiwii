import re
from http import HTTPStatus
from typing import Optional

from kiwii.architecture.server.api.auth.shared.models import AuthenticationHandlerParams
from kiwii.architecture.server.api.shared.consts import HTTP_HEADER_AUTHORIZATION
from kiwii.architecture.server.data.data import get_data_layer
from kiwii.architecture.server.shared.models import Response
from kiwii.data.data_structures.credentials import CredentialsDataStructure

AUTHORIZATION_PATTERN: re.Pattern = re.compile(r"^Basic (.*)$")
ADMIN_CREDENTIALS: Optional[CredentialsDataStructure] = None


def handle(auth_params: AuthenticationHandlerParams) -> Response:
    """
    Performs `HTTP Basic Authorization`:
    - reads HTTP Authorization header
    - validates the value format
    - compares the credential value with actual credentials
    """

    # one-off admin credential load into memory
    global ADMIN_CREDENTIALS
    if ADMIN_CREDENTIALS is None:
        ADMIN_CREDENTIALS = get_data_layer().retrieve(CredentialsDataStructure)

    # make sure authorization header is present
    authorization_header_value = auth_params.route_params.request.headers.get(HTTP_HEADER_AUTHORIZATION, "")
    if not authorization_header_value:
        return Response(status=HTTPStatus.UNAUTHORIZED)

    # make sure authorization value is valid
    authorization_value_match = AUTHORIZATION_PATTERN.match(authorization_header_value)
    if not authorization_value_match:
        return Response(status=HTTPStatus.UNAUTHORIZED)

    # make sure credentials match
    if not ADMIN_CREDENTIALS.match(authorization_value_match.groups()[0]):
        return Response(status=HTTPStatus.UNAUTHORIZED)

    return auth_params.route_handler(auth_params.route_params)

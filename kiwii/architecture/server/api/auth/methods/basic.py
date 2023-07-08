import re
from http import HTTPStatus

from kiwii.architecture.server.api.auth.shared.hash_utils import get_hash
from kiwii.architecture.server.api.auth.shared.models import AuthenticationHandlerParams
from kiwii.architecture.server.api.shared.consts import HTTP_HEADER_AUTHORIZATION
from kiwii.architecture.server.shared.models import Response
from kiwii.data.data import retrieve
from kiwii.data.data_structures.user import AdminDataStructure

AUTHORIZATION_PATTERN: re.Pattern = re.compile(r"^Basic (.*)$")


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

    user_data_structure = retrieve(AdminDataStructure)

    # make sure credentials match
    if get_hash(authorization_value_match.groups()[0]) != user_data_structure.credentials:
        return Response(status=HTTPStatus.UNAUTHORIZED)

    return auth_params.route_handler(auth_params.route_params)

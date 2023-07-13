import json
from http import HTTPStatus

from kiwii.architecture.server.api import register
from kiwii.architecture.server.api.auth import authenticate
from kiwii.architecture.server.api.auth.auth import authorize
from kiwii.architecture.server.api.shared.models import AuthenticationMethod, RouteParams
from kiwii.architecture.server.shared.models import Response
from kiwii.architecture.shared.routes import STATUS_ROUTE, StatusRouteParams


@register(STATUS_ROUTE)
@authenticate(AuthenticationMethod.BASIC)
@authorize
def status(_: RouteParams[StatusRouteParams]) -> Response:
    """
    Server status route handler. Returns JSON which contains general server status (e.g. configuration, available
    agents, etc.).

    TODO implement
    """

    return Response(status=HTTPStatus.OK, body=json.dumps({}))

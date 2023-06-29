import json
from http import HTTPMethod, HTTPStatus

from kiwii.architecture.server.api import register
from kiwii.architecture.server.api.auth import authenticate
from kiwii.architecture.server.api.shared.models import AuthenticationMethod, RouteParams
from kiwii.architecture.server.shared.models import Response
from kiwii.architecture.shared.route_paths import STATUS_ROUTE_PATTERN


@register(HTTPMethod.GET, STATUS_ROUTE_PATTERN)
@authenticate(AuthenticationMethod.BASIC)
def status(_: RouteParams) -> Response:
    return Response(status=HTTPStatus.OK, body=json.dumps({}))

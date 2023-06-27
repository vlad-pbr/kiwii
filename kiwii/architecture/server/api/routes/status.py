import json
from http import HTTPMethod, HTTPStatus
from typing import Tuple

from kiwii.architecture.server.api import register
from kiwii.architecture.server.shared.models import Response
from kiwii.architecture.shared.route_paths import STATUS_ROUTE_PATH


@register(HTTPMethod.GET, STATUS_ROUTE_PATH)
def status(_: Tuple) -> Response:
    return Response(status=HTTPStatus.OK, body=json.dumps({}))

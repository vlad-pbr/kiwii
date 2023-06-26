import json
from http import HTTPMethod, HTTPStatus
from typing import Tuple

from kiwii.architecture.server.api import register
from kiwii.architecture.server.shared.models import Response, Route
from kiwii.architecture.shared.endpoints import STATUS_ENDPOINT


@register(Route(HTTPMethod.GET, STATUS_ENDPOINT))
def status(_: Tuple) -> Response:
    return Response(status=HTTPStatus.OK, body=json.dumps({}))

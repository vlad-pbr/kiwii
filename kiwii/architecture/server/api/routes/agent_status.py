import json
from http import HTTPMethod, HTTPStatus
from typing import Tuple

from kiwii.architecture.server.api import register
from kiwii.architecture.server.shared.models import Response
from kiwii.architecture.shared.route_paths import AGENT_STATUS_ROUTE_PATH


@register(HTTPMethod.GET, AGENT_STATUS_ROUTE_PATH)
def agent_status(path_params: Tuple) -> Response:
    return Response(
        status=HTTPStatus.OK,
        body=json.dumps({
            "id": path_params[0]
        })
    )

from http import HTTPMethod, HTTPStatus
from typing import Tuple
import json

from kiwii.architecture.server.api import register
from kiwii.architecture.server.shared.models import Response, Route
from kiwii.architecture.shared.endpoints import AGENT_STATUS_ENDPOINT


@register(Route(HTTPMethod.GET, AGENT_STATUS_ENDPOINT))
def agent_status(path_params: Tuple) -> Response:
    return Response(
        status=HTTPStatus.OK,
        body=json.dumps({
            "id": path_params[0]
        })
    )

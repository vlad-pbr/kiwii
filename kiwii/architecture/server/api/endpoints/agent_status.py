from http import HTTPMethod, HTTPStatus
from typing import Tuple
import json

from kiwii.architecture.server.api import register
from kiwii.architecture.shared.endpoints import AGENT_STATUS_ENDPOINT


@register(HTTPMethod.GET, AGENT_STATUS_ENDPOINT)
def agent_status(path_params: Tuple) -> Tuple[HTTPStatus, str]:
    return HTTPStatus.OK, json.dumps({
        "id": path_params[0]
    })

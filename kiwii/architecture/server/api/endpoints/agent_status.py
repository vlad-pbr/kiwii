from http import HTTPMethod, HTTPStatus
from typing import Tuple
import json

from kiwii.architecture.server.api import register


@register(HTTPMethod.GET, r"/agent/([a-zA-Z0-9]{16})/status")
def agent_status(path_params: Tuple) -> Tuple[HTTPStatus, str]:
    return HTTPStatus.OK, json.dumps({
        "id": path_params[0]
    })

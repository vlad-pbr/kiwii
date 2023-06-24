from http import HTTPMethod, HTTPStatus
from typing import Tuple
import json

from kiwii.architecture.server.api import register


@register(HTTPMethod.GET, r"/status")
def status(_) -> Tuple[HTTPStatus, str]:
    return HTTPStatus.OK, json.dumps({})

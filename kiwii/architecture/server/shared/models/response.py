from http import HTTPStatus
from typing import NamedTuple, Optional


class Response(NamedTuple):
    status: HTTPStatus
    body: Optional[str] = None

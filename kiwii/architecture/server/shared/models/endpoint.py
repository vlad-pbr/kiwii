from http import HTTPMethod
from typing import NamedTuple


class Endpoint(NamedTuple):
    method: HTTPMethod
    path: str

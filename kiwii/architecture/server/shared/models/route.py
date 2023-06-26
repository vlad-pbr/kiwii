from http import HTTPMethod
from typing import NamedTuple


class Route(NamedTuple):
    method: HTTPMethod
    path: str

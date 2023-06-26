from http import HTTPMethod
from typing import NamedTuple


class Request(NamedTuple):
    method: HTTPMethod
    path: str

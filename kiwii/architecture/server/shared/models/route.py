from http import HTTPMethod
from re import Pattern
from typing import NamedTuple


class Route(NamedTuple):
    method: HTTPMethod
    pattern: Pattern

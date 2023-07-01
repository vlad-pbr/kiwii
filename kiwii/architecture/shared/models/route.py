from http import HTTPMethod
from re import Pattern
from typing import NamedTuple, Type

from kiwii.architecture.shared.types import RouteParamsType


class Route(NamedTuple):
    """
    Describes one or multiple API endpoints.

    This is different from the `Endpoint` model:
    - `Endpoint` represents a client request (requested HTTP method and URI)
    - `Route` represents a pattern which can match multiple `Endpoints`s for one specific HTTP method.

    `Endpoint`s are regex matched against existing `Route`s until a match is found. `Route` patters may include
    capture groups which serve as path parameters which are then delegated to the associated `Route` handler.
    """

    method: HTTPMethod
    pattern: Pattern
    path: str
    params_type: Type[RouteParamsType]

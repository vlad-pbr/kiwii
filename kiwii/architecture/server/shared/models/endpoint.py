from http import HTTPMethod
from typing import NamedTuple


class Endpoint(NamedTuple):
    """
    Describes a client request endpoint (e.g. `GET` request for `/status` URI)

    This is different from the `Route` model:
    - `Endpoint` represents a client request (requested HTTP method and URI)
    - `Route` represents a pattern which can match multiple `Endpoints`s for one specific HTTP method.
    """

    method: HTTPMethod
    path: str

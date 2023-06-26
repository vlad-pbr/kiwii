from typing import NamedTuple

from .route import Route


class Request(NamedTuple):
    route: Route

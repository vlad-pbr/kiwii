from typing import NamedTuple, Generic

from kiwii.architecture.server.shared.models import Request
from kiwii.architecture.shared.types import RouteParamsType


class RouteParams(Generic[RouteParamsType], NamedTuple):
    """Parameters provided to route handlers."""

    request: Request
    path_params: RouteParamsType

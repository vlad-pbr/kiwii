from typing import NamedTuple, Tuple

from kiwii.architecture.server.shared.models import Request


class RouteParams(NamedTuple):
    """Parameters provided to route handlers."""

    request: Request
    path_params: Tuple

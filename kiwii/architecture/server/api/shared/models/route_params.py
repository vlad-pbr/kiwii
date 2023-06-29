from typing import NamedTuple, Tuple

from kiwii.architecture.server.shared.models import Request


class RouteParams(NamedTuple):
    request: Request
    path_params: Tuple

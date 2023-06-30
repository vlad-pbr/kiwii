from typing import NamedTuple

from kiwii.architecture.server.api.shared.models import RouteParams
from kiwii.architecture.server.api.shared.types import RouteHandler


class AuthenticationHandlerParams(NamedTuple):
    route_params: RouteParams
    route_handler: RouteHandler

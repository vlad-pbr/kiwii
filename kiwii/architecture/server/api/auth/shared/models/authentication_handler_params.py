from typing import NamedTuple

from kiwii.architecture.server.api.shared.types import RouteHandler


class AuthenticationHandlerParams(NamedTuple):
    handler: RouteHandler

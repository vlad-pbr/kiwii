from typing import Callable

from kiwii.architecture.server.api.auth.shared.models import AuthenticationHandlerParams
from kiwii.architecture.server.api.shared.types import RouteHandler

AuthenticationHandler = Callable[[AuthenticationHandlerParams], RouteHandler]

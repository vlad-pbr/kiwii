from typing import Callable

from kiwii.architecture.server.api.shared.models import RouteParams
from kiwii.architecture.server.shared.models import Response

RouteHandler = Callable[[RouteParams], Response]
RouteDecorator = Callable[[RouteHandler], RouteHandler]

from typing import Callable, Tuple

from kiwii.architecture.server.shared.models import Response

EndpointHandler = Callable[[Tuple], Response]
EndpointDecoratorReturn = Callable[[EndpointHandler], EndpointHandler]

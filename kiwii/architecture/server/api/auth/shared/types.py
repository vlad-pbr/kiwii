from typing import Callable

from kiwii.architecture.server.api.auth.shared.models import AuthenticationHandlerParams
from kiwii.architecture.server.shared.models import Response

AuthenticationHandler = Callable[[AuthenticationHandlerParams], Response]

from dataclasses import dataclass
from typing import Generic, Optional

from kiwii.architecture.server.shared.models import Request
from kiwii.architecture.shared.models import Route
from kiwii.architecture.shared.types import RouteParamsType
from .authorization_metadata import AuthorizationMetadata


@dataclass
class RouteParams(Generic[RouteParamsType]):
    """Parameters provided to route handlers."""

    request: Request
    path_params: RouteParamsType
    route: Route
    authorization: Optional[AuthorizationMetadata] = None

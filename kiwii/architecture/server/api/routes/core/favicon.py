from http import HTTPStatus

from kiwii.architecture.server.api import register
from kiwii.architecture.server.api.shared.models import RouteParams
from kiwii.architecture.server.api.shared.models.content_type import ContentType
from kiwii.architecture.server.logic.favicon.favicon import get_favicon_bytes
from kiwii.architecture.server.shared.models import Response
from kiwii.architecture.shared.routes import FAVICON_ROUTE, FaviconRouteParams


@register(FAVICON_ROUTE)
def favicon(_: RouteParams[FaviconRouteParams]) -> Response:
    """
    Returns kiwii favicon. Cute.
    """

    response = Response(status=HTTPStatus.OK, body=get_favicon_bytes())
    response.set_content_type(ContentType.XICON)

    return response

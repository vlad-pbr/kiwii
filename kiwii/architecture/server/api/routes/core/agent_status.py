import json
from http import HTTPMethod, HTTPStatus

from kiwii.architecture.server.api import register
from kiwii.architecture.server.api.shared.models import RouteParams
from kiwii.architecture.server.shared.models import Response
from kiwii.architecture.shared.route_paths import AGENT_STATUS_ROUTE_PATTERN


@register(HTTPMethod.GET, AGENT_STATUS_ROUTE_PATTERN)
def agent_status(params: RouteParams) -> Response:
    """
    Agent status route handler. Returns JSON which contains general agent status (e.g. configuration, available
    devices, etc.).

    TODO implement
    """

    return Response(
        status=HTTPStatus.OK,
        body=json.dumps({
            "id": params.path_params[0]
        })
    )

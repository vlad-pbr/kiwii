import json
from http import HTTPStatus

from kiwii.architecture.server.api import register
from kiwii.architecture.server.api.shared.models import RouteParams
from kiwii.architecture.server.shared.models import Response
from kiwii.architecture.shared.routes import AGENT_STATUS_ROUTE, AgentStatusRouteParams


@register(AGENT_STATUS_ROUTE)
def agent_status(params: RouteParams[AgentStatusRouteParams]) -> Response:
    """
    Agent status route handler. Returns JSON which contains general agent status (e.g. configuration, available
    devices, etc.).

    TODO implement
    """

    return Response(
        status=HTTPStatus.OK,
        body=json.dumps({
            "id": params.path_params.id
        })
    )

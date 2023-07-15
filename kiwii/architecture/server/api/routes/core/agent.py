from http import HTTPStatus

from kiwii.architecture.server.api import register
from kiwii.architecture.server.api.auth import authenticate
from kiwii.architecture.server.api.shared.models import RouteParams, AuthenticationMethod
from kiwii.architecture.server.shared.models import Response
from kiwii.architecture.shared.routes import AGENT_POST_ROUTE, AgentPostRouteParams, AGENT_STATUS_ROUTE, \
    AgentStatusRouteParams


@register(AGENT_POST_ROUTE)
@authenticate(AuthenticationMethod.BASIC)
def agent_post(_: RouteParams[AgentPostRouteParams]) -> Response:
    """
    New agent creation handler. Returns JSON which contains the new agent ID.

    TODO implement
    """

    # TODO register new agent with the server
    # TODO add authorization for agent to post its status

    return Response(status=HTTPStatus.NOT_IMPLEMENTED)


@register(AGENT_STATUS_ROUTE)
def agent_status(_: RouteParams[AgentStatusRouteParams]) -> Response:
    """
    Agent status route handler. Returns JSON which contains general agent status (e.g. configuration, available
    devices, etc.).

    TODO implement
    """

    return Response(status=HTTPStatus.NOT_IMPLEMENTED)

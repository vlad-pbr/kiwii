import re
from typing import Set

from kiwii.architecture.server.shared.models import Route, Request

# TODO single header?
AUTHENTICATION_HEADER_USERNAME: str = "Username"
AUTHENTICATION_HEADER_PASSWORD: str = "Password"

# TODO delegate to actual storage
AUTHENTICATION_CREDENTIALS_USERNAME: str = "admin"
AUTHENTICATION_CREDENTIALS_PASSWORD: str = "admin"

_do_not_authenticate: Set[Route] = set()


def disable_authentication(route: Route) -> None:
    _do_not_authenticate.add(route)


def authenticate_request(request: Request) -> bool:

    # check routes with disabled authentication
    for not_authenticated_route in _do_not_authenticate:  # TODO there must be a more efficient way...
        if not_authenticated_route.method == request.route.method and re.match(not_authenticated_route.path,
                                                                               request.route.path):
            return True

    # perform authentication
    username = request.headers.get(AUTHENTICATION_HEADER_USERNAME, "")
    password = request.headers.get(AUTHENTICATION_HEADER_PASSWORD, "")
    if username != AUTHENTICATION_CREDENTIALS_USERNAME or password != AUTHENTICATION_CREDENTIALS_PASSWORD:
        return False

    return True

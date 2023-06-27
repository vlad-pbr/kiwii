from email.message import Message
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


def authenticate_user(headers: Message) -> bool:

    # perform authentication
    username = headers.get(AUTHENTICATION_HEADER_USERNAME, "")
    password = headers.get(AUTHENTICATION_HEADER_PASSWORD, "")
    if username == AUTHENTICATION_CREDENTIALS_USERNAME and password == AUTHENTICATION_CREDENTIALS_PASSWORD:
        return True

    return False


def authenticate_request(route: Route, request: Request) -> bool:

    # if route authentication is disabled - allow
    if route in _do_not_authenticate:
        return True

    # if user is authenticated - allow
    if authenticate_user(request.headers):
        return True

    return False

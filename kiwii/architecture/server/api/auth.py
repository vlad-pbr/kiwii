import re
import base64
from email.message import Message
from typing import Set

from kiwii.architecture.server.shared.models import Route, Request

AUTHORIZATION_HEADER: str = "Authorization"
AUTHORIZATION_PATTERN: re.Pattern = re.compile(r"^Basic (.*)$")

# TODO delegate to actual storage
AUTHENTICATION_CREDENTIALS: str = base64.b64encode(b"admin:admin").decode()

_do_not_authenticate: Set[Route] = set()


def disable_authentication(route: Route) -> None:
    _do_not_authenticate.add(route)


def authenticate_user(headers: Message) -> bool:

    # make sure authorization header is present
    authorization_value: str = headers.get(AUTHORIZATION_HEADER, "")
    if not authorization_value:
        return False

    # make sure authorization value is valid
    authorization_match = AUTHORIZATION_PATTERN.match(authorization_value)
    if not authorization_match:
        return False

    # make sure credentials match
    if authorization_match.groups()[0] != AUTHENTICATION_CREDENTIALS:
        return False

    return True


def authenticate_request(route: Route, request: Request) -> bool:

    # if route authentication is disabled - allow
    if route in _do_not_authenticate:
        return True

    # if user is authenticated - allow
    if authenticate_user(request.headers):
        return True

    return False

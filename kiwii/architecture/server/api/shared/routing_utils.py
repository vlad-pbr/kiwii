"""
Utilities related to HTTP routing which are used by routes.
"""

from email.message import Message
from http import HTTPStatus

from kiwii.architecture.server.api.shared.consts import HTTP_HEADER_LOCATION
from kiwii.architecture.server.shared.models import Response


def redirect(url: str) -> Response:
    """Returns HTTP Permanent Redirect response to given URL."""

    headers = Message()
    headers.add_header(HTTP_HEADER_LOCATION, url)

    return Response(status=HTTPStatus.PERMANENT_REDIRECT, headers=headers)

from __future__ import annotations

from dataclasses import dataclass
from email.message import Message
from http import HTTPStatus
from typing import Optional, AnyStr

from kiwii.architecture.server.api.shared.consts import HTTP_HEADER_LOCATION, HTTP_HEADER_CONTENT_TYPE
from kiwii.architecture.server.api.shared.models.content_type import ContentType


@dataclass
class Response:
    """
    HTTP application layer response returned by route handlers to the client.
    """

    status: HTTPStatus
    headers: Optional[Message] = None
    body: Optional[AnyStr] = None

    @staticmethod
    def redirect(url: str) -> Response:
        """Returns HTTP Permanent Redirect response to given URL."""

        headers = Message()
        headers.add_header(HTTP_HEADER_LOCATION, url)

        return Response(status=HTTPStatus.PERMANENT_REDIRECT, headers=headers)

    def set_content_type(self, content_type: ContentType) -> None:
        """Sets content type header for current `Response` object."""

        if self.headers is None:
            self.headers = Message()

        self.headers.add_header(HTTP_HEADER_CONTENT_TYPE, content_type)

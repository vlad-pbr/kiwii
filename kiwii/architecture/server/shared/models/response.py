from email.message import Message
from http import HTTPStatus
from typing import NamedTuple, Optional


class Response(NamedTuple):
    """
    HTTP application layer response returned by route handlers to the client.
    """

    status: HTTPStatus
    headers: Optional[Message] = None
    body: Optional[str] = None

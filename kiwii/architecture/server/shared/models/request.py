from email.message import Message
from typing import NamedTuple

from .endpoint import Endpoint


class Request(NamedTuple):
    """
    Full user API request model which includes the `Endpoint` (HTTP method and URI) as well as headers and other
    HTTP application layer data.
    """

    endpoint: Endpoint
    headers: Message

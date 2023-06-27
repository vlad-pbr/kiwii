from email.message import Message
from typing import NamedTuple

from .endpoint import Endpoint


class Request(NamedTuple):
    endpoint: Endpoint
    headers: Message

import base64
from dataclasses import dataclass
from typing import Dict

from kiwii.architecture.shared.headers import HTTP_HEADER_AUTHORIZATION


@dataclass
class UserCredentials:
    """User credentials container."""

    username: str
    password: str

    def as_authorization_basic_string(self) -> str:
        """Encodes credentials in HTTP Basic Authorization header (base64 of `username:password`)."""

        return base64.b64encode(f"{self.username}:{self.password}".encode()).decode()

    def as_authorization_basic_header(self) -> Dict[str, str]:
        """Returns a headers dictionary with HTTP Basic Authorization credentials encoded in."""

        return {HTTP_HEADER_AUTHORIZATION: f"Basic {self.as_authorization_basic_string()}"}

import base64
from typing import NamedTuple


class UserCredentials(NamedTuple):
    """User credentials container."""

    username: str
    password: str

    def as_authorization_basic(self) -> str:
        """Encodes credentials in HTTP Basic Authorization header (base64 of `username:password`)."""

        return base64.b64encode(f"{self.username}:{self.password}".encode()).decode()

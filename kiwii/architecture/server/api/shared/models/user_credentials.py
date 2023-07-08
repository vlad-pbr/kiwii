from typing import NamedTuple


class UserCredentials(NamedTuple):
    """Admin user credentials container."""

    username: str
    password: str

from enum import Enum, auto


class AuthenticationMethod(Enum):
    """Existing authentication methods for `Route`s."""

    BASIC = auto()

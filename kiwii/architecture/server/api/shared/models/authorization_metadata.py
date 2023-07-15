from typing import NamedTuple

from kiwii.architecture.server.data.data_structures.credentials import CredentialsDataStructure


class AuthorizationMetadata(NamedTuple):
    """Metadata populated by authorization handlers upon successful authorization."""

    credentials: CredentialsDataStructure

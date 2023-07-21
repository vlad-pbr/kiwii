from dataclasses import dataclass

from kiwii.architecture.shared.models.serveraddress import ServerAddress
from kiwii.architecture.shared.models.user_credentials import UserCredentials


@dataclass
class RemoteServerParams:
    """
    `dataclass` wrapper around the parameters required for agent registration with a remote kiwii server.
    """

    address: ServerAddress
    credentials: UserCredentials
    re_register: bool

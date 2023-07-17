from dataclasses import dataclass


@dataclass
class RemoteServerConnection:
    """
    `dataclass` wrapper around the parameters required for agent registration with a remote kiwii server.
    """

    host: str
    port: int
    username: str
    password: str

from dataclasses import dataclass
from typing import Tuple


@dataclass
class ServerAddress:
    """
    `NamedTuple` wrapper around the parameters required by the `http.server.HTTPServer` constructor which
    are used as the server address.
    """

    host: str
    port: int

    def as_tuple(self) -> Tuple[str, int]:
        return self.host, self.port

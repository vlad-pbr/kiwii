from typing import NamedTuple


class ServerAddress(NamedTuple):
    """
    `NamedTuple` wrapper around the parameters required by the `http.server.HTTPServer` constructor which
    are used as the server address.
    """

    host: str
    port: str

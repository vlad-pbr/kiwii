"""
Kiwii agent static class. Not actually a class as static classes are not pythonic.
"""

from typing import Optional

from kiwii.architecture.agent.shared.models import RemoteServerConnection


def start(
        remote_server_connection: Optional[RemoteServerConnection],
        log_level: str
):
    """Starts the kiwii agent using provided parameters."""

    pass

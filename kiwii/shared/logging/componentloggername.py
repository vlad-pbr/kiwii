from enum import StrEnum


class ComponentLoggerName(StrEnum):
    """Logger names for the core parts of kiwii architecture."""

    SERVER = "server"
    API = "api"

    SERVER_DATA = "server-data"

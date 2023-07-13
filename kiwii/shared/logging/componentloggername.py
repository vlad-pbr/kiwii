from enum import StrEnum


class ComponentLoggerName(StrEnum):
    """Logger names for the core parts of kiwii architecture."""

    SERVER = "server"
    SERVER_DATA = "server-data"

    API = "api"
    API_AUTH = "api-auth"

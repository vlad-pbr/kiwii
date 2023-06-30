"""
Regex patterns used across the architecture. These serve as a single source of truth for everything related
to entity patterns. This is used by route related modules (e.g. server which defines routes, agent which can generate
values from given patterns in order to query the API, etc.).
"""

AGENT_ID_PATTERN: str = r"[a-zA-Z0-9]{16}"

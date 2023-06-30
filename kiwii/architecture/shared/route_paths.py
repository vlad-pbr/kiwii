"""
Single source of truth for everything related to API route paths. Here, we define regex patterns for
API routes (for the server module) and endpoints which should be used to query the API (for the client and
agent modules).

A clear distinction should be made between the `pattern` value and `path` value:
- `pattern` value is a generic regex which can match multiple API endpoints
- `path` value is a string which represents a single endpoint which can be queried

So `pattern` and `path` correlate, but have two different semantic meanings.
"""

from kiwii.architecture.shared.patterns import AGENT_ID_PATTERN

STATUS_ROUTE_PATTERN: str = r"^/status$"
STATUS_ROUTE_PATH: str = r"/status"

AGENT_STATUS_ROUTE_PATTERN: str = fr"^/agent/({AGENT_ID_PATTERN})/status$"
AGENT_STATUS_ROUTE_PATH: str = r"/agent/{id}/status"

DOC_ROUTE_PATTERN: str = r"^/doc(?:/|/(?:([a-z0-9._]*)\.html))?$"
DOC_ROUTE_PATH: str = r"/doc"

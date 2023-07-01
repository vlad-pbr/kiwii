"""
Single source of truth for everything related to API routes and how to query them. Here, we define regex patterns for
API routes (for the server module) and endpoints which should be used to query the API (for the client and
agent modules).

A clear distinction should be made between the `pattern` value and `path` value:
- `pattern` value is a generic regex which can match multiple API endpoints
- `path` value is a string which represents a single endpoint which can be queried

So `pattern` and `path` correlate, but have two different semantic meanings.
"""

import re
from http import HTTPMethod
from typing import NamedTuple

from kiwii.architecture.shared.models.route import Route
from kiwii.architecture.shared.patterns import AGENT_ID_PATTERN

StatusRouteParams = NamedTuple("StatusRouteParams", [])
STATUS_ROUTE = Route(
    method=HTTPMethod.GET,
    pattern=re.compile(r"^/status$"),
    path=r"/status",
    params_type=StatusRouteParams
)

AgentStatusRouteParams = NamedTuple("AgentStatusRouteParams", [("id", str)])
AGENT_STATUS_ROUTE = Route(
    method=HTTPMethod.GET,
    pattern=re.compile(fr"^/agent/({AGENT_ID_PATTERN.pattern})/status$"),
    path=r"/agent/{id}/status",
    params_type=AgentStatusRouteParams
)

DocRouteParams = NamedTuple("DocRouteParams", [("module", str)])
DOC_ROUTE = Route(
    method=HTTPMethod.GET,
    pattern=re.compile(r"^/doc(?:/|/([a-z0-9._]*)\.html)?$"),
    path=r"/doc",
    params_type=DocRouteParams
)

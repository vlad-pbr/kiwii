from kiwii.architecture.shared.patterns import AGENT_ID_PATTERN

STATUS_ROUTE_PATTERN: str = r"^/status$"
STATUS_ROUTE_PATH: str = r"/status"

AGENT_STATUS_ROUTE_PATTERN: str = fr"^/agent/({AGENT_ID_PATTERN})/status$"
AGENT_STATUS_ROUTE_PATH: str = r"/agent/{id}/status"

DOC_ROUTE_PATTERN: str = r"^/doc(?:/|/(?:([a-z0-9._]*)\.html))?$"
DOC_ROUTE_PATH: str = r"/doc"

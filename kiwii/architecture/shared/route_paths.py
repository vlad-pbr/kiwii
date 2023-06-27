from kiwii.architecture.shared.patterns import AGENT_ID_PATTERN

STATUS_ROUTE_PATH: str = r"/status"
AGENT_STATUS_ROUTE_PATH: str = fr"/agent/({AGENT_ID_PATTERN})/status"

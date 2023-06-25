from kiwii.architecture.shared.patterns import AGENT_ID_PATTERN

STATUS_ENDPOINT: str = r"/status"
AGENT_STATUS_ENDPOINT: str = fr"/agent/({AGENT_ID_PATTERN})/status"

from typing import List

from kiwii.architecture.shared.models import Route
from kiwii.architecture.shared.routes import AGENT_POST_ROUTE

ADMIN_USER_ALLOWED_ROUTES: List[Route] = [AGENT_POST_ROUTE]

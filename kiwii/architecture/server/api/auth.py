import re
from typing import Set

from kiwii.architecture.server.shared.models import Route

_do_not_authenticate: Set[Route] = set()


def disable_authentication(route: Route) -> None:
    _do_not_authenticate.add(route)


def requires_authentication(route: Route) -> bool:
    for not_authenticated_route in _do_not_authenticate:  # TODO there must be a more efficient way...
        if not_authenticated_route.method == route.method and re.match(not_authenticated_route.path, route.path):
            return False
    return True

from http import HTTPMethod

from kiwii.architecture.server.api import register


@register(HTTPMethod.GET, "/status")
def status():
    return "chilling"

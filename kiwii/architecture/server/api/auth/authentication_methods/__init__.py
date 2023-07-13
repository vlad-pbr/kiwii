"""
Authentication method handlers for available authentication methods.

Authentication method handler acts as a wrapper around a route in a sense that it has access to the route
parameters in order to use them for validation. In case of an authentication error, it itself can respond
with a `Response` model including the return status. In case authentication checks out, authentication method
handler should call the route handler itself in order to properly handle the request.
"""

from .basic import basic

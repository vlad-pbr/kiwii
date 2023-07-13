"""
Kiwii API routes.

A distinction must be made between `core` routes and `optional` routes:
- `core` routes are registered on API initialization no matter what
- `optional` routes are registered upon user request when starting the server (e.g. documentation route)

Routes are registered by simply importing them using python's `import` statement which triggers the registration
decorators.

Routes are decorated using API route registration decorator and can also be decorated using authentication and
authorization decorators in order to secure routes behind permission management. When using these decorators, the order
matters:

- When matching an endpoint to a route, the API simply calls the route handler, meaning the handler must already
  be decorated with permission management decorators.
- Authorization decorator matches credentials to an existing user/agent and populates route parameters with
  relevant authorization metadata.
- Authentication decorator uses the authorization metadata populated by the authorization decorator in order
  to match credentials to permissions, meaning authentication MUST come before authorization.

Therefore, the following order of decorators must be kept:

@register
@authenticate
@authorize
"""
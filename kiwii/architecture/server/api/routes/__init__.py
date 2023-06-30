"""
Kiwii API routes.

A distinction must be made between `core` routes and `optional` routes:
- `core` routes are registered on API initialization no matter what
- `optional` routes are registered upon user request when starting the server (e.g. documentation route)

Routes are registered by simply importing them using python's `import` statement which triggers the registration
decorators.
"""
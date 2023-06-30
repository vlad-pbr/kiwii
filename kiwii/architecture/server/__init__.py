"""
Kiwii server logic.

It includes:
- Custom-built `http.server.HTTPServer` with TLS option
- FastAPI-like API declaration of endpoints (called routes) using decorators
- Authorization options for routes using decorators
- Kiwii documentation route using `pydoc` HTML rendering of module documentation (opt-in)
- CLI parser for server control
"""

from .server import start

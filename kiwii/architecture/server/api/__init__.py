"""
Kiwii server API related logic, which includes:
- `Route` registration
- `Endpoint` to `Route` resolution
- Authorization for the registered `Route`s
"""

from .api import initialize, register, handle

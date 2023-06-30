"""
Everything related to running the server itself, such as:
- Setting up the server address and SSL socket (if requested)
- Initializing API
- Setting log levels for underlying entities
"""

from .server import start

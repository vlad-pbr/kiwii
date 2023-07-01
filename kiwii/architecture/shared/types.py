"""
Common python typing constants used across the architecture.
"""

from typing import TypeVar, NamedTuple

RouteParamsType = TypeVar("RouteParamsType", bound=NamedTuple)

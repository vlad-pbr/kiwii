"""
Common python typing constants used across all core parts of the architecture.
"""

from typing import Callable, List, Tuple

Parser = Callable[[List[str], Tuple], None]

"""
Server data layer static class.

Not actually a class as static classes are not pythonic.

# TODO don't like this, refactor
"""

from pathlib import Path
from typing import Optional

from kiwii.data.data import Data
from kiwii.shared.logging.componentloggername import ComponentLoggerName

_data: Optional[Data] = None


def get_data_layer() -> Optional[Data]:
    """Returns server data layer object or None if it was not initialized."""

    return _data


def initialize(filepath: str, log_level: str) -> None:
    """Initializes data layer with given parameters."""

    global _data

    _data = Data(Path(filepath), ComponentLoggerName.SERVER_DATA, log_level)

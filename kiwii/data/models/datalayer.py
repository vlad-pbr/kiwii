from dataclasses import dataclass, field
from typing import Dict

from kiwii.data.data_structures.datastructure import DataStructure


@dataclass
class DataLayer:
    """Top level data container which stores the underlying data structures in a dictionary."""

    data_structures: Dict[str, DataStructure] = field(default_factory=dict)

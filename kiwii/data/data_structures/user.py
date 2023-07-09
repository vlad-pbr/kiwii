from dataclasses import dataclass

from .datastructure import DataStructure


@dataclass
class AdminDataStructure(DataStructure):
    """Single data structure to represent admin account credentials."""

    hash: str
    salt: str

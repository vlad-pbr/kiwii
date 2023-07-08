"""
Base data layer class for instantiation by various components.

# TODO convert to reusable class
"""

from typing import Dict, Type, TypeVar, Optional

from kiwii.data.data_structures.datastructure import DataStructure

_DataStructure = TypeVar("_DataStructure", bound=DataStructure)

# TODO use top level data layer
# TODO persist to disk
data: Dict[str, DataStructure] = {}


def store(data_structure: _DataStructure) -> None:
    """Stores provided data structure to storage"""

    data[data_structure.__class__.__name__] = data_structure


def retrieve(data_structure_type: Type[_DataStructure]) -> Optional[_DataStructure]:
    """Returns requested data structure or `None` if one is not currently present in storage"""

    return data.get(data_structure_type.__name__, None)

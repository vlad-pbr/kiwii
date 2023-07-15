"""
Python types shared across data logic.
"""

from __future__ import annotations

from typing import TypeVar

from kiwii.data.data_structures.datastructure import DataStructure

TDataStructure = TypeVar("TDataStructure", bound=DataStructure)

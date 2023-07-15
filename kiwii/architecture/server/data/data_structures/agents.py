from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from kiwii.architecture.server.data.models.agent import Agent
from kiwii.data.data_structures.datastructure import DataStructure


@dataclass
class AgentsDataStructure(DataStructure):
    """Container for storing existing agents."""

    agents: Dict[str, Agent]

from __future__ import annotations

from dataclasses import dataclass

from kiwii.architecture.shared.models.serveraddress import ServerAddress
from kiwii.architecture.shared.models.user_credentials import UserCredentials
from kiwii.data.data_structures.datastructure import DataStructure


@dataclass
class RemoteServerStructure(DataStructure):
    """Remote server parameters storage."""

    address: ServerAddress
    credentials: UserCredentials

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Optional

from kiwii.shared.hash_utils import get_hash
from kiwii.data.data_structures.datastructure import DataStructure


@dataclass
class CredentialsDataStructure(DataStructure):
    """Single data structure to represent user/agent credentials."""

    hash: str
    salt: str

    @staticmethod
    def from_literal(plaintext_credentials: str, salt: Optional[str] = None) -> CredentialsDataStructure:
        """Returns a new `CredentialsDataStructure` constructed from provided plaintext credentials."""

        # if salt was not provided, generate one
        if not salt:
            salt: str = get_hash(str(random.random()))

        return CredentialsDataStructure(
            hash=get_hash(plaintext_credentials, salt),
            salt=salt
        )

    def match(self, plaintext_credentials: str) -> bool:
        """Matches provided plaintext credentials with current credentials using the current salt."""

        return get_hash(plaintext_credentials, self.salt) == self.hash

"""
Common hash utilities used across the kiwii API authentication process.
"""

import hashlib
from typing import Optional


def get_hash(data: str, salt: Optional[str] = None) -> str:
    return hashlib.sha512(f"{data}{salt if salt is not None else ''}".encode()).hexdigest()

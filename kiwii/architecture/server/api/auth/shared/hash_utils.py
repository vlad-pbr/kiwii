"""
Common hash utilities used across the kiwii API authentication process.
"""

import hashlib


def get_hash(data: str) -> str:
    return hashlib.sha512(data.encode()).hexdigest()

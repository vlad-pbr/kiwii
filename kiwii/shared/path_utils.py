"""
Path related utilities used across all core parts of the architecture.
"""

import urllib.parse
import os
from typing import AnyStr


def urijoin(base: AnyStr, *uris: AnyStr) -> AnyStr:
    """
    Wrapper around `urllib.parse.urljoin` which ensures that `uris` are always appended to `base`.
    In most cases it will just append the strings, but I wanted a single by-design URL path combination function
    which handles any other edge cases.

    NOTE: `urllib.parse.urljoin`'s `allow_fragments` (also known os anchors) is jank when it comes to combining URIs,
    therefore, for now, this function sets it to `False` for all URIs which tells urllib.parse.urljoin` to,
    counter-intuitively, not care about fragments in the provided URI and keep them as part of the path. Make sure that
    if you do provide a fragment, it is located in the final URI.
    """

    url = base
    for uri in uris:
        url = urllib.parse.urljoin(f"{url.strip().rstrip('/')}/", uri.strip().lstrip('/'), allow_fragments=False)

    return url


def normalize(path: AnyStr) -> AnyStr:
    """
    Normalizes `path` by using `os.path.normpath` and `os.path.normcase` to define a single standard for path strings.
    """

    return os.path.normcase(os.path.normpath(path))

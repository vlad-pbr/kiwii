"""
Constants related to module documentation generation
"""

import platform
import urllib.parse

from kiwii import __pythondocs__ as kiwii_url

KIWII_URL = urllib.parse.urlparse(kiwii_url)
PYTHON_STDLIB_URL = urllib.parse.urlparse(
    f"https://github.com/python/cpython/tree/{'.'.join(platform.python_version_tuple()[:2])}/Lib"
)

from typing import Optional
from pathlib import Path

FAVICON: Optional[bytes] = None


def get_favicon_bytes() -> bytes:
    """Returns favicon image icon as bytes."""

    global FAVICON

    # one-time favicon load into memory
    # TODO move favicon to static files
    if FAVICON is None:
        with open(Path(__file__).parent / "favicon.ico", "rb") as favicon_file:
            FAVICON = favicon_file.read()

    return FAVICON

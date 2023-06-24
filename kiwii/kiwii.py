"""
I'm Kiwii
"""

from pathlib import Path

from kiwii.parser.parser import parse

__version__ = "0.1.0"


def cli():
    parse(Path(__file__).stem, __doc__, __version__)


if __name__ == "__main__":
    cli()

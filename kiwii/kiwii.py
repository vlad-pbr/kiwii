#!/usr/bin/env python3.11

"""
I'm Kiwii
"""

from kiwii.parser.parser import parse

__version__ = "0.1.0"


def cli():
    parse(__doc__, __version__)


if __name__ == "__main__":
    cli()

"""
Uses `argparse` to parse kiwii local agent related CLI calls (local agent configuration).
"""

from argparse import ArgumentParser
from typing import List, Tuple

from kiwii.shared.argparse_utils import parse_prog


def parse(args: List[str], prog: Tuple):
    """Local agent machine configuration."""

    parser = ArgumentParser(
        prog=parse_prog(prog),
        description=parse.__doc__
    )

    parser.parse_args(args)

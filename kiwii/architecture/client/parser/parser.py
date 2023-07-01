"""
Uses `argparse` to parse kiwii client related CLI calls (server interaction).
"""

from argparse import ArgumentParser
from typing import List, Tuple

from kiwii.shared.argparse_utils import parse_prog


def parse(args: List[str], prog: Tuple):
    """Interaction with a kiwii server."""

    parser = ArgumentParser(
        prog=parse_prog(prog),
        description=parse.__doc__
    )

    parser.parse_args(args)

"""
Uses `argparse` to parse kiwii local agent related CLI calls (local agent configuration).
"""

from argparse import ArgumentParser
from dataclasses import asdict
from typing import List, Tuple

from kiwii.architecture.agent.parser.consts import SUBPARSERACTION_ACTION, SUBPARSER_START, SUBPARSER_TO_CLI
from kiwii.shared.argparse_utils import parse_prog, delegate_prog


def parse(args: List[str], prog: Tuple):
    """Local agent machine configuration."""

    parser = ArgumentParser(
        prog=parse_prog(prog),
        description=parse.__doc__
    )

    subparsers = parser.add_subparsers(**asdict(SUBPARSERACTION_ACTION))

    subparsers.add_parser(**asdict(SUBPARSER_START), add_help=False)

    known_args, unknown_args = parser.parse_known_args(args)
    known_args_dict = vars(known_args)

    if known_args_dict[SUBPARSERACTION_ACTION.dest]:
        SUBPARSER_TO_CLI[known_args_dict[SUBPARSERACTION_ACTION.dest]](
            unknown_args,
            delegate_prog(prog, known_args_dict[SUBPARSERACTION_ACTION.dest])
        )

"""
Top-level kiwii parser.
"""

from argparse import ArgumentParser, RawTextHelpFormatter
from dataclasses import asdict
from typing import Tuple

from kiwii.parser.consts import SUBPARSER_CLIENT, SUBPARSER_SERVER, SUBPARSER_AGENT, \
    SUBPARSER_TO_CLI, SUBPARSERACTION_ARCHITECTURE, ARGUMENT_VERSION
from kiwii.shared.argparse_utils import to_flag, parse_prog, delegate_prog


def parse(prog: Tuple, description: str, version: str):
    """Uses `argparse` to parse top-level CLI calls. This is the actual entrypoint for the entire CLI."""

    parser = ArgumentParser(
        prog=parse_prog(prog),
        description=description,
        formatter_class=RawTextHelpFormatter
    )

    # top level kiwii args
    parser.add_argument(to_flag(ARGUMENT_VERSION.dest), **asdict(ARGUMENT_VERSION))

    # architecture elements subparsers
    subparsers = parser.add_subparsers(**asdict(SUBPARSERACTION_ARCHITECTURE))
    subparsers.add_parser(**asdict(SUBPARSER_CLIENT), add_help=False)
    subparsers.add_parser(**asdict(SUBPARSER_SERVER), add_help=False)
    subparsers.add_parser(**asdict(SUBPARSER_AGENT), add_help=False)

    known_args, unknown_args = parser.parse_known_args()
    known_args_dict = vars(known_args)

    if known_args_dict[ARGUMENT_VERSION.dest]:
        print(version)
    elif known_args_dict[SUBPARSERACTION_ARCHITECTURE.dest]:
        SUBPARSER_TO_CLI[known_args_dict[SUBPARSERACTION_ARCHITECTURE.dest]](
            unknown_args,
            delegate_prog(prog, known_args_dict[SUBPARSERACTION_ARCHITECTURE.dest])
        )
    elif unknown_args:
        parser.parse_args(unknown_args)

from argparse import ArgumentParser
from dataclasses import asdict
from typing import List

from kiwii.architecture.server.parser.consts import SUBPARSER_START, SUBPARSERACTION_ACTION, SUBPARSER_TO_CLI


def parse(args: List[str]):
    """Uses `argparse` to parse kiwii server related CLI calls (e.g. starting, stopping, etc.)."""

    parser = ArgumentParser()

    subparsers = parser.add_subparsers(**asdict(SUBPARSERACTION_ACTION))

    subparsers.add_parser(**asdict(SUBPARSER_START), add_help=False)

    known_args, unknown_args = parser.parse_known_args(args)
    known_args_dict = vars(known_args)

    if known_args_dict[SUBPARSERACTION_ACTION.dest]:
        SUBPARSER_TO_CLI[known_args_dict[SUBPARSERACTION_ACTION.dest]](unknown_args)

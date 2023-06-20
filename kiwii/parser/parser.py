from argparse import ArgumentParser
from dataclasses import asdict

from kiwii.parser.consts import SUBPARSER_CLIENT, SUBPARSER_SERVER, SUBPARSER_AGENT, \
    SUBPARSER_TO_CLI, SUBPARSERACTION_ARCHITECTURE, ARGUMENT_VERSION
from kiwii.shared.argparse_utils import to_flag


def parse(file: str, description: str, version: str):

    parser = ArgumentParser(
        prog=file,
        description=description
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
        SUBPARSER_TO_CLI[known_args_dict[SUBPARSERACTION_ARCHITECTURE.dest]](unknown_args)
    elif unknown_args:
        parser.parse_args(unknown_args)

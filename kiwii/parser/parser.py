from argparse import ArgumentParser
from dataclasses import asdict

from kiwii.parser.subcommands import SUBCOMMAND_CLIENT, SUBCOMMAND_SERVER, SUBCOMMAND_AGENT, \
    SUBCOMMAND_TO_CLI
from kiwii.parser.consts import KIWII_ARGPARSE_ARCHITECTURE_ARGUMENT, KIWII_ARGPARSE_VERSION_ARGUMENT
from kiwii.shared.argparse_utils import to_flag, to_destination, ARGPARSE_STORE_TRUE_ACTION


def parse(file: str, description: str, version: str):

    parser = ArgumentParser(
        prog=file,
        description=description,
    )

    # top level kiwii args
    parser.add_argument(
        to_flag(KIWII_ARGPARSE_VERSION_ARGUMENT),
        action=ARGPARSE_STORE_TRUE_ACTION,
        dest=to_destination(KIWII_ARGPARSE_VERSION_ARGUMENT),
        help="print version and exit")

    # architecture elements subparsers
    subparsers = parser.add_subparsers(
        dest=to_destination(KIWII_ARGPARSE_ARCHITECTURE_ARGUMENT),
        help="architecture elements")
    subparsers.add_parser(**asdict(SUBCOMMAND_CLIENT))
    subparsers.add_parser(**asdict(SUBCOMMAND_SERVER))
    subparsers.add_parser(**asdict(SUBCOMMAND_AGENT))

    known_args, unknown_args = parser.parse_known_args()
    known_args_dict = vars(known_args)

    if known_args_dict[to_destination(KIWII_ARGPARSE_VERSION_ARGUMENT)]:
        print(version)
    elif known_args_dict[to_destination(KIWII_ARGPARSE_ARCHITECTURE_ARGUMENT)]:
        SUBCOMMAND_TO_CLI[known_args_dict[to_destination(KIWII_ARGPARSE_ARCHITECTURE_ARGUMENT)]](unknown_args)
    elif unknown_args:
        parser.parse_args(unknown_args)

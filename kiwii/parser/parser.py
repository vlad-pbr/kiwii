from argparse import ArgumentParser
from dataclasses import asdict

from kiwii.parser.subcommands import ARGPARSE_SUBCOMMAND, SUBCOMMAND_CLIENT, SUBCOMMAND_SERVER, SUBCOMMAND_AGENT, \
    SUBCOMMAND_TO_CLI


def parse(description: str):

    parser = ArgumentParser(
        prog=__file__,
        description=description,
    )
    subparsers = parser.add_subparsers(dest=ARGPARSE_SUBCOMMAND)

    subparser_client = subparsers.add_parser(**asdict(SUBCOMMAND_CLIENT))
    subparser_server = subparsers.add_parser(**asdict(SUBCOMMAND_SERVER))
    subparser_agent = subparsers.add_parser(**asdict(SUBCOMMAND_AGENT))

    known_args, unknown_args = parser.parse_known_args()
    known_args_dict = vars(known_args)

    if known_args_dict[ARGPARSE_SUBCOMMAND]:
        SUBCOMMAND_TO_CLI[known_args_dict[ARGPARSE_SUBCOMMAND]](unknown_args)
    elif unknown_args:
        parser.parse_args(unknown_args)

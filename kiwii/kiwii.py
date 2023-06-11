#!/usr/bin/env python3.11

"""
I'm Kiwii
"""

from argparse import ArgumentParser, Namespace
from dataclasses import dataclass, asdict


@dataclass
class Subcommand:
    name: str
    help: str


# kiwii subcommands
SUBCOMMAND_CLIENT = Subcommand(
    name="client",
    help="server interaction"
)
SUBCOMMAND_SERVER = Subcommand(
    name="server",
    help="server execution and management"
)
SUBCOMMAND_AGENT = Subcommand(
    name="agent",
    help="agent execution and management"
)

# argparse consts
ARGPARSE_SUBCOMMAND: str = "subcommand"


def main():
    parser: ArgumentParser = ArgumentParser(
        prog=__file__,
        description=__doc__,
    )
    subparsers = parser.add_subparsers(dest=ARGPARSE_SUBCOMMAND)

    # kiwii entrypoint subcommands
    subparser_client = subparsers.add_parser(**asdict(SUBCOMMAND_CLIENT))
    subparser_server = subparsers.add_parser(**asdict(SUBCOMMAND_SERVER))
    subparser_agent = subparsers.add_parser(**asdict(SUBCOMMAND_AGENT))

    args: Namespace = parser.parse_args()

    print(args)

    exit(0)


if __name__ == "__main__":
    main()

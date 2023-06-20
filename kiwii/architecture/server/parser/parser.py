from argparse import ArgumentParser
from dataclasses import asdict
from typing import List

from kiwii.architecture.server.parser.consts import SUBCOMMAND_START, SUBPARSERACTION_ACTION


def parse(args: List[str]):

    parser = ArgumentParser()

    subparsers = parser.add_subparsers(**asdict(SUBPARSERACTION_ACTION))

    subparsers.add_parser(**asdict(SUBCOMMAND_START))

    parser.parse_args(args)

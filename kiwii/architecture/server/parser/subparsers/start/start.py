from argparse import ArgumentParser
from dataclasses import asdict
from typing import List

from kiwii.architecture.server.server import start
from kiwii.shared.argparse_utils import to_flag

from kiwii.architecture.server.parser.subparsers.start.consts import ARGUMENT_HOST, ARGUMENT_PORT


def parse(args: List[str]):

    parser = ArgumentParser()

    # basic server args
    parser.add_argument(to_flag(ARGUMENT_HOST.dest), **asdict(ARGUMENT_HOST))
    parser.add_argument(to_flag(ARGUMENT_PORT.dest), **asdict(ARGUMENT_PORT))

    args = parser.parse_args(args)
    args_dict = vars(args)

    start(args_dict[ARGUMENT_HOST.dest], args_dict[ARGUMENT_PORT.dest])

"""
Uses `argparse` to parse kiwii agent starting related CLI calls (e.g. kiwii remote server endpoint, log level, etc.)
"""

from argparse import ArgumentParser
from dataclasses import asdict
from typing import List, Tuple, Optional

from kiwii.architecture.agent.agent.agent import start
from kiwii.architecture.agent.parser.subparsers.start.consts import ARGUMENT_HOST, ARGUMENT_PORT, ARGUMENT_USERNAME, \
    ARGUMENT_PASSWORD, ARGUMENT_LOG_LEVEL
from kiwii.architecture.agent.shared.models import RemoteServerConnection
from kiwii.shared.argparse_utils import parse_prog, to_flag, evaluate_inclusivity, Inclusivity
from kiwii.shared.models import Argument


def parse(rsc_args: List[str], prog: Tuple):
    """Start local kiwii agent with provided configuration."""

    parser = ArgumentParser(
        prog=parse_prog(prog),
        description=parse.__doc__
    )

    # basic agent args
    parser.add_argument(to_flag(ARGUMENT_HOST.dest), **asdict(ARGUMENT_HOST))
    parser.add_argument(to_flag(ARGUMENT_PORT.dest), **asdict(ARGUMENT_PORT))
    parser.add_argument(to_flag(ARGUMENT_USERNAME.dest), **asdict(ARGUMENT_USERNAME))
    parser.add_argument(to_flag(ARGUMENT_PASSWORD.dest), **asdict(ARGUMENT_PASSWORD))
    parser.add_argument(to_flag(ARGUMENT_LOG_LEVEL.dest), **asdict(ARGUMENT_LOG_LEVEL))

    args = parser.parse_args(rsc_args)
    args_dict = vars(args)

    # make sure remote server connection arguments are inclusive
    remote_server_connection: Optional[RemoteServerConnection] = None
    rsc_args: List[Argument] = [ARGUMENT_HOST, ARGUMENT_PORT, ARGUMENT_USERNAME, ARGUMENT_PASSWORD]
    match evaluate_inclusivity(args_dict, *rsc_args):
        case Inclusivity.NonInclusive:
            parser.error(
                f"none or all of the following arguments must be defined: {', '.join([arg.dest for arg in rsc_args])}"
            )
        case Inclusivity.InclusiveAndDefined:
            remote_server_connection = RemoteServerConnection(
                host=args_dict[ARGUMENT_HOST.dest],
                port=args_dict[ARGUMENT_PORT.dest],
                username=args_dict[ARGUMENT_USERNAME.dest],
                password=args_dict[ARGUMENT_PASSWORD.dest]
            )

    start(
        remote_server_connection,
        args_dict[ARGUMENT_LOG_LEVEL.dest]
    )

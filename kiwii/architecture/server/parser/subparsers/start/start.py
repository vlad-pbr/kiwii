"""
Uses `argparse` to parse kiwii server starting related CLI calls (e.g. reading TLS certificate, log level, etc.)
"""

from argparse import ArgumentParser
from dataclasses import asdict
from typing import List, Optional, Tuple

from kiwii.architecture.server import start
from kiwii.architecture.shared.models import ServerAddress
from kiwii.architecture.shared.models.user_credentials import UserCredentials
from kiwii.architecture.server.parser.subparsers.start.consts import ARGUMENT_HOST, ARGUMENT_PORT, ARGUMENT_TLS_CERT, \
    ARGUMENT_TLS_KEY, ARGUMENT_LOG_LEVEL, ARGUMENT_DOC, ARGUMENT_USERNAME, ARGUMENT_PASSWORD
from kiwii.architecture.server.shared.models import SSLCertChain
from kiwii.shared.argparse_utils import to_flag, parse_prog, evaluate_inclusivity, Inclusivity


def parse(args: List[str], prog: Tuple):
    """Start local kiwii server with provided configuration."""

    # TODO cors

    parser = ArgumentParser(
        prog=parse_prog(prog),
        description=parse.__doc__
    )

    # basic server args
    parser.add_argument(to_flag(ARGUMENT_HOST.dest), **asdict(ARGUMENT_HOST))
    parser.add_argument(to_flag(ARGUMENT_PORT.dest), **asdict(ARGUMENT_PORT))
    parser.add_argument(to_flag(ARGUMENT_TLS_CERT.dest), **asdict(ARGUMENT_TLS_CERT))
    parser.add_argument(to_flag(ARGUMENT_TLS_KEY.dest), **asdict(ARGUMENT_TLS_KEY))
    parser.add_argument(to_flag(ARGUMENT_LOG_LEVEL.dest), **asdict(ARGUMENT_LOG_LEVEL))
    parser.add_argument(to_flag(ARGUMENT_DOC.dest), **asdict(ARGUMENT_DOC))
    parser.add_argument(to_flag(ARGUMENT_USERNAME.dest), **asdict(ARGUMENT_USERNAME))
    parser.add_argument(to_flag(ARGUMENT_PASSWORD.dest), **asdict(ARGUMENT_PASSWORD))

    args = parser.parse_args(args)
    args_dict = vars(args)

    # make sure that if one user credentials related argument is provided, both username and password keys are provided
    credentials: Optional[UserCredentials] = None
    match evaluate_inclusivity(args_dict, ARGUMENT_USERNAME, ARGUMENT_PASSWORD):
        case Inclusivity.NonInclusive:
            parser.error(
                f"both {to_flag(ARGUMENT_USERNAME.dest)} and {to_flag(ARGUMENT_PASSWORD.dest)} must be defined"
            )
        case Inclusivity.InclusiveAndDefined:
            credentials = UserCredentials(
                username=args_dict[ARGUMENT_USERNAME.dest],
                password=args_dict[ARGUMENT_PASSWORD.dest]
            )

    start(
        ServerAddress(host=args_dict[ARGUMENT_HOST.dest], port=args_dict[ARGUMENT_PORT.dest]),
        SSLCertChain(
            certfile=args_dict[ARGUMENT_TLS_CERT.dest],
            keyfile=args_dict[ARGUMENT_TLS_KEY.dest]
        ),
        args_dict[ARGUMENT_LOG_LEVEL.dest],
        args_dict[ARGUMENT_DOC.dest],
        credentials
    )

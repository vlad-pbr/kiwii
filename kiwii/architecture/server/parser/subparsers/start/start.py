"""
Uses `argparse` to parse kiwii server starting related CLI calls (e.g. reading TLS certificate, log level, etc.)
"""

from argparse import ArgumentParser
from dataclasses import asdict
from typing import List, Optional, Tuple

from kiwii.architecture.server import start
from kiwii.architecture.server.api.shared.models.user_credentials import UserCredentials
from kiwii.architecture.server.parser.subparsers.start.consts import ARGUMENT_HOST, ARGUMENT_PORT, ARGUMENT_TLS_CERT, \
    ARGUMENT_TLS_KEY, ARGUMENT_LOG_LEVEL, ARGUMENT_DOC, ARGUMENT_USERNAME, ARGUMENT_PASSWORD
from kiwii.architecture.server.shared.models import SSLCertChain, ServerAddress
from kiwii.shared.argparse_utils import to_flag, parse_prog


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

    # make sure that if one tls related argument is provided, both public and private keys are provided
    ssl_cert_chain: Optional[SSLCertChain] = None
    if not bool(args_dict[ARGUMENT_TLS_CERT.dest]) == bool(args_dict[ARGUMENT_TLS_KEY.dest]):
        parser.error(f"both {to_flag(ARGUMENT_TLS_CERT.dest)} and {to_flag(ARGUMENT_TLS_KEY.dest)} must be defined")
    elif bool(args_dict[ARGUMENT_TLS_CERT.dest]):
        ssl_cert_chain = SSLCertChain(
            certfile=args_dict[ARGUMENT_TLS_CERT.dest],
            keyfile=args_dict[ARGUMENT_TLS_KEY.dest]
        )

    # make sure that if one user credentials related argument is provided, both username and password keys are provided
    credentials: Optional[UserCredentials] = None
    if not bool(args_dict[ARGUMENT_USERNAME.dest]) == bool(args_dict[ARGUMENT_PASSWORD.dest]):
        parser.error(f"both {to_flag(ARGUMENT_USERNAME.dest)} and {to_flag(ARGUMENT_PASSWORD.dest)} must be defined")
    elif bool(args_dict[ARGUMENT_USERNAME.dest]):
        credentials = UserCredentials(
            username=args_dict[ARGUMENT_USERNAME.dest],
            password=args_dict[ARGUMENT_PASSWORD.dest]
        )

    start(
        ServerAddress(host=args_dict[ARGUMENT_HOST.dest], port=args_dict[ARGUMENT_PORT.dest]),
        ssl_cert_chain,
        args_dict[ARGUMENT_LOG_LEVEL.dest],
        args_dict[ARGUMENT_DOC.dest],
        credentials
    )

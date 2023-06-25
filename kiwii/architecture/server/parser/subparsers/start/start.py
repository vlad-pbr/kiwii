from argparse import ArgumentParser
from dataclasses import asdict
from typing import List, Optional

from kiwii.architecture.server import start
from kiwii.architecture.server.parser.subparsers.start.consts import ARGUMENT_HOST, ARGUMENT_PORT, ARGUMENT_SSL_CERT, \
    ARGUMENT_SSL_KEY, ARGUMENT_LOG_LEVEL
from kiwii.architecture.server.shared.models import SSLCertChain, ServerAddress
from kiwii.shared.argparse_utils import to_flag


def parse(args: List[str]):

    parser = ArgumentParser()

    # basic server args
    parser.add_argument(to_flag(ARGUMENT_HOST.dest), **asdict(ARGUMENT_HOST))
    parser.add_argument(to_flag(ARGUMENT_PORT.dest), **asdict(ARGUMENT_PORT))
    parser.add_argument(to_flag(ARGUMENT_SSL_CERT.dest), **asdict(ARGUMENT_SSL_CERT))
    parser.add_argument(to_flag(ARGUMENT_SSL_KEY.dest), **asdict(ARGUMENT_SSL_KEY))
    parser.add_argument(to_flag(ARGUMENT_LOG_LEVEL.dest), **asdict(ARGUMENT_LOG_LEVEL))

    args = parser.parse_args(args)
    args_dict = vars(args)

    # make sure that if one ssl related argument is provided, both public and private keys are provided
    ssl_cert_chain: Optional[SSLCertChain] = None
    if not bool(args_dict[ARGUMENT_SSL_CERT.dest]) == bool(args_dict[ARGUMENT_SSL_KEY.dest]):
        parser.error(f"both {to_flag(ARGUMENT_SSL_CERT.dest)} and {to_flag(ARGUMENT_SSL_KEY.dest)} must be defined")
    elif bool(args_dict[ARGUMENT_SSL_CERT.dest]):
        ssl_cert_chain = SSLCertChain(
            certfile=args_dict[ARGUMENT_SSL_CERT.dest],
            keyfile=args_dict[ARGUMENT_SSL_KEY.dest]
        )

    start(
        ServerAddress(host=args_dict[ARGUMENT_HOST.dest], port=args_dict[ARGUMENT_PORT.dest]),
        ssl_cert_chain,
        args_dict[ARGUMENT_LOG_LEVEL.dest]
    )

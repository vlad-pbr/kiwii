"""
Constants (mostly `argparse` related models) for the kiwii server start CLI parser.
"""

from logging import getLevelNamesMapping, INFO

from kiwii.shared.argparse_utils import to_destination
from kiwii.shared.models import Argument, StoreTrueArgument

ARGUMENT_HOST = Argument(
    dest=to_destination("host"),
    type=str,
    default="0.0.0.0",
    required=False,
    choices=None,
    help="address to listen on",
)

ARGUMENT_PORT = Argument(
    dest=to_destination("port"),
    type=int,
    default="8080",
    required=False,
    choices=None,
    help="port to listen on",
)

ARGUMENT_TLS_CERT = Argument(
    dest=to_destination("tls-cert"),
    type=str,
    default=None,
    required=True,
    choices=None,
    help="path to certificate public key in PEM format"
)

ARGUMENT_TLS_KEY = Argument(
    dest=to_destination("tls-key"),
    type=str,
    default=None,
    required=True,
    choices=None,
    help="path to certificate private key in PEM format"
)

ARGUMENT_LOG_LEVEL = Argument(
    dest=to_destination("log-level"),
    type=str,
    default={v: k for k, v in getLevelNamesMapping().items()}[INFO],
    required=False,
    choices=[k for k in getLevelNamesMapping().keys()],
    help="log level the server will log at"
)

ARGUMENT_USERNAME = Argument(
    dest=to_destination("username"),
    type=str,
    default=None,
    required=False,
    choices=None,
    help="authentication username"
)

ARGUMENT_PASSWORD = Argument(
    dest=to_destination("password"),
    type=str,
    default=None,
    required=False,
    choices=None,
    help="authentication password"
)

ARGUMENT_DOC = StoreTrueArgument(
    dest=to_destination("doc"),
    help="expose documentation API endpoint"
)

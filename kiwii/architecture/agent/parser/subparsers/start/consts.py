"""
Constants (mostly `argparse` related models) for the kiwii agent start CLI parser.
"""

from logging import getLevelNamesMapping, INFO

from kiwii.shared.argparse_utils import to_destination
from kiwii.shared.models import Argument, StoreTrueArgument

ARGUMENT_HOST = Argument(
    dest=to_destination("host"),
    type=str,
    default=None,
    required=False,
    choices=None,
    help="one time kiwii remote server host",
)

ARGUMENT_PORT = Argument(
    dest=to_destination("port"),
    type=int,
    default=None,
    required=False,
    choices=None,
    help="one time kiwii remote server port",
)

ARGUMENT_USERNAME = Argument(
    dest=to_destination("username"),
    type=str,
    default=None,
    required=False,
    choices=None,
    help="one time authentication username for registration with kiwii remote server"
)

ARGUMENT_PASSWORD = Argument(
    dest=to_destination("password"),
    type=str,
    default=None,
    required=False,
    choices=None,
    help="one time authentication password for registration with kiwii remote server"
)

ARGUMENT_RE_REGISTER = StoreTrueArgument(
    dest=to_destination("re-register"),
    help="perform re-registration with provided parameters in case agent is already registered with a server"
)

ARGUMENT_LOG_LEVEL = Argument(
    dest=to_destination("log-level"),
    type=str,
    default={v: k for k, v in getLevelNamesMapping().items()}[INFO],
    required=False,
    choices=[k for k in getLevelNamesMapping().keys()],
    help="log level the agent will log at"
)

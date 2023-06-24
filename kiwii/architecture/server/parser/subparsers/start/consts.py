from kiwii.shared.argparse_utils import to_destination
from kiwii.shared.models import Argument

ARGUMENT_HOST = Argument(
    dest=to_destination("host"),
    type=str,
    default="0.0.0.0",
    required=False,
    help="address to listen on",
)

ARGUMENT_PORT = Argument(
    dest=to_destination("port"),
    type=int,
    default="8080",
    required=False,
    help="port to listen on",
)

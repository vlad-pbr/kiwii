from typing import Dict, Callable, List

from kiwii.architecture.agent.parser.parser import parse as agent_parser
from kiwii.architecture.client.parser.parser import parse as client_parser
from kiwii.architecture.server.parser.parser import parse as server_parser
from kiwii.shared.argparse_utils import to_destination
from kiwii.shared.models import Subparser
from kiwii.shared.models import SubparserAction
from kiwii.shared.models.storetrueargument import StoreTrueArgument


SUBPARSERACTION_ARCHITECTURE = SubparserAction(
    dest=to_destination("architecture"),
    help="architecture elements",
)


SUBPARSER_CLIENT = Subparser(
    name="client",
    help="server interaction"
)
SUBPARSER_SERVER = Subparser(
    name="server",
    help="server execution and management"
)
SUBPARSER_AGENT = Subparser(
    name="agent",
    help="agent execution and management"
)


ARGUMENT_VERSION = StoreTrueArgument(
    dest=to_destination("version"),
    help="print version and exit",
)


SUBPARSER_TO_CLI: Dict[str, Callable[[List[str]], None]] = {
    SUBPARSER_CLIENT.name: client_parser,
    SUBPARSER_SERVER.name: server_parser,
    SUBPARSER_AGENT.name: agent_parser
}

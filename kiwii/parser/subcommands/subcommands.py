from typing import Dict, Callable, List

from kiwii.subcommands import client, server, agent
from kiwii.models import Subcommand

SUBCOMMAND_CLIENT = Subcommand(
    name="client",
    help="server interaction"
)
SUBCOMMAND_SERVER = Subcommand(
    name="server",
    help="server execution and management"
)
SUBCOMMAND_AGENT = Subcommand(
    name="agent",
    help="agent execution and management"
)

SUBCOMMAND_TO_CLI: Dict[str, Callable[[List[str]], None]] = {
    SUBCOMMAND_CLIENT.name: client.cli,
    SUBCOMMAND_SERVER.name: server.cli,
    SUBCOMMAND_AGENT.name: agent.cli
}

ARGPARSE_SUBCOMMAND: str = "subcommand"

"""
Constants (mostly `argparse` related models) for the kiwii agent CLI parser.
"""

from typing import Dict

from kiwii.shared.models import SubparserAction, Subparser
from kiwii.shared.types import Parser

from kiwii.architecture.agent.parser.subparsers.start import parse as start_parser

SUBPARSERACTION_ACTION = SubparserAction(
    dest="action",
    help="available actions"
)
SUBPARSER_START = Subparser(
    name="start",
    help="start agent connection with remote kiwii server"
)

SUBPARSER_TO_CLI: Dict[str, Parser] = {
    SUBPARSER_START.name: start_parser,
}

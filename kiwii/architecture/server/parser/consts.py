"""
Constants (mostly `argparse` related models) for the kiwii server CLI parser.
"""

from typing import Dict

from kiwii.architecture.server.parser.subparsers.start import parse as start_parser
from kiwii.shared.models import Subparser, SubparserAction
from kiwii.shared.types import Parser

SUBPARSERACTION_ACTION = SubparserAction(
    dest="action",
    help="available actions"
)


SUBPARSER_START = Subparser(
    name="start",
    help="start local kiwii server"
)


SUBPARSER_TO_CLI: Dict[str, Parser] = {
    SUBPARSER_START.name: start_parser,
}

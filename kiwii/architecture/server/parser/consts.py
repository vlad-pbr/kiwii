"""
Constants (mostly `argparse` related models) for the kiwii server CLI parser.
"""

from typing import Dict, Callable, List

from kiwii.shared.models import Subparser, SubparserAction
from kiwii.architecture.server.parser.subparsers.start import parse as start_parser


SUBPARSERACTION_ACTION = SubparserAction(
    dest="action",
    help="available actions"
)


SUBPARSER_START = Subparser(
    name="start",
    help="start local kiwii server"
)


SUBPARSER_TO_CLI: Dict[str, Callable[[List[str]], None]] = {
    SUBPARSER_START.name: start_parser,
}

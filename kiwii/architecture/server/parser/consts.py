from kiwii.shared.models import Subparser, SubparserAction

SUBPARSERACTION_ACTION = SubparserAction(
    dest="action",
    help="available actions"
)


SUBCOMMAND_START = Subparser(
    name="start",
    help="start local kiwii server"
)

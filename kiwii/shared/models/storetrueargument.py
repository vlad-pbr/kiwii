from dataclasses import dataclass

from kiwii.shared.argparse_utils import ARGPARSE_STORE_TRUE_ACTION


@dataclass
class StoreTrueArgument:
    dest: str
    help: str
    action: str = ARGPARSE_STORE_TRUE_ACTION

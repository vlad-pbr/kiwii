"""
Models shared across the architecture.

Some models are dataclass wrappers around `argparse` arguments and parsers. This approach has two advantages:
- Makes sure no field is left unfilled
- Ensures the argument value can be taken via `dest` parameter directly from the `argparse.Namespace` (avoids typos
  and is more generic)
- Can be easily unpacked directly into `ArgumentParser` methods using `asdict` which ensures all fields were
  provided
"""

from .subparser import Subparser
from .subparseraction import SubparserAction
from .argument import Argument
from .storetrueargument import StoreTrueArgument

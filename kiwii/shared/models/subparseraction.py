from dataclasses import dataclass


@dataclass
class SubparserAction:
    """Dedicated model for an `argparse` subparser."""

    dest: str
    help: str

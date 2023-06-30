from dataclasses import dataclass


@dataclass
class Subparser:
    """Dedicated model for an `argparse` subparser."""

    name: str
    help: str

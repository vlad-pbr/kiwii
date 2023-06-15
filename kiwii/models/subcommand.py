from dataclasses import dataclass


@dataclass
class Subcommand:
    name: str
    help: str

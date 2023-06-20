from dataclasses import dataclass


@dataclass
class Argument:
    dest: str
    action: str
    help: str

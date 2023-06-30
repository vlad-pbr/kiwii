from dataclasses import dataclass
from typing import Optional, Callable, Any, Iterable


@dataclass
class Argument:
    """Dedicated model for an `argparse` argument with value."""

    dest: str
    type: Optional[Callable]
    default: Any
    required: bool
    help: str
    choices: Optional[Iterable]

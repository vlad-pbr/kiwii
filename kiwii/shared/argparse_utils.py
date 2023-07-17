"""
Common utilities used across subparsers of the CLI.
"""

from enum import Enum, auto
from typing import Tuple, Dict, Any

from kiwii.shared.models import Argument


class Inclusivity(Enum):
    """Inclusivity state of arguments."""

    InclusiveAndDefined = auto()
    InclusiveAndUndefined = auto()
    NonInclusive = auto()


def to_destination(argument: str) -> str:
    """Ensures provided argument complies with the `dest` format of argparse argument."""

    return argument.lstrip("-").replace('-', '_')


def to_flag(argument: str) -> str:
    """Ensures provided argument complies with the CLI long flag format of argparse argument."""

    return f"--{argument.replace('_', '-')}"


def parse_prog(prog: Tuple) -> str:
    """Parses 'prog' tuple for `argparse.ArgumentParser` `prog` argument for user-friendliness."""

    return ' '.join(prog)


def delegate_prog(base_prog: Tuple, subparser: str):
    """Appends `subparser` to given `base_prog` tuple to delegate `prog` to underlying subparser."""

    return base_prog + (subparser,)


def evaluate_inclusivity(args_dict: Dict[str, Any], *args: Argument) -> Inclusivity:
    """
    Evaluates provided `args` in `args_dict` and reports on their inclusivity, meaning:
    - all args were provided (InclusiveAndDefined)
    - none of the args were provided (InclusiveAndUndefined)
    - some of the args were provided (NonInclusive)
    """

    if len({bool(args_dict[arg.dest]) for arg in args}) > 1:
        return Inclusivity.NonInclusive

    return Inclusivity.InclusiveAndDefined if bool(args_dict[args[0].dest]) else Inclusivity.InclusiveAndUndefined


ARGPARSE_STORE_TRUE_ACTION: str = "store_true"

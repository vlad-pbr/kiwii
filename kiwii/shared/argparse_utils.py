"""
Common utilities used across subparsers of the CLI.
"""

from typing import Tuple


def to_destination(argument: str) -> str:
    """Ensures provided argument complies with the `dest` format of argparse argument."""

    return argument.replace('-', '_')


def to_flag(argument: str) -> str:
    """Ensures provided argument complies with the CLI long flag format of argparse argument."""

    return f"--{argument.replace('_', '-')}"


def parse_prog(prog: Tuple) -> str:
    """Parses 'prog' tuple for `argparse.ArgumentParser` `prog` argument for user-friendliness."""

    return ' '.join(prog)


def delegate_prog(base_prog: Tuple, subparser: str):
    """Appends `subparser` to given `base_prog` tuple to delegate `prog` to underlying subparser."""

    return base_prog + (subparser,)


ARGPARSE_STORE_TRUE_ACTION: str = "store_true"

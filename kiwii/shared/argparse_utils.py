"""
Common utilities used across subparsers of the CLI.
"""


def to_destination(argument: str) -> str:
    """Ensures provided argument complies with the `dest` format of argparse argument."""

    return argument.replace('-', '_')


def to_flag(argument: str) -> str:
    """Ensures provided argument complies with the CLI long flag format of argparse argument."""

    return f"--{argument.replace('_', '-')}"


ARGPARSE_STORE_TRUE_ACTION: str = "store_true"

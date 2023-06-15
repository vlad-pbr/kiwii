def to_destination(argument: str):
    return argument.replace('-', '_')


def to_flag(argument: str):
    return f"--{argument.replace('_', '-')}"


ARGPARSE_STORE_TRUE_ACTION: str = "store_true"

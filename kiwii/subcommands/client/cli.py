from argparse import ArgumentParser
from typing import List


def cli(args: List[str]):

    parser = ArgumentParser()

    parser.parse_args(args)

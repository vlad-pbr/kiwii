from argparse import ArgumentParser
from typing import List


def parse(args: List[str]):

    parser = ArgumentParser()

    parser.parse_args(args)

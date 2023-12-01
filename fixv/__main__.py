""" Replace the absolute path in the executable files in an virtual env,
so that it works after moved.
"""

import argparse
from pathlib import Path

from .jobs import repair


def parse_args():
    parser = argparse.ArgumentParser(__package__, description=__doc__)
    parser.add_argument('root', type=Path, help='venv root path')
    return parser.parse_args()


def main():
    args = parse_args()
    # print(args)
    # return
    root: Path = args.root

    repair(root)


if __name__ == '__main__':
    main()

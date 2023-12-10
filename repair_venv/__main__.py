""" Replace the absolute path in the executable files in an virtual env,
so that it works after moved.
"""

import argparse
import sys
from pathlib import Path

from .core import repair
from .log import logger

parser = argparse.ArgumentParser(
    prog=__package__ if len(sys.argv) == 1 else sys.argv[1], description=__doc__
)
parser.add_argument('root', type=Path, help='venv root path')
args = parser.parse_args(sys.argv[2:])

logger.debug(f'{args=}')
root: Path = args.root

repair(root)

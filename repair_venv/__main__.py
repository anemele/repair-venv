""" Replace the absolute path in the executable files in an virtual env,
so that it works after moved.
"""

import argparse
from pathlib import Path

from .core import repair
from .log import logger

parser = argparse.ArgumentParser(prog=__package__, description=__doc__)
parser.add_argument('root', type=Path, help='venv root path')
args = parser.parse_args()

logger.debug(f'{args=}')
root: Path = args.root

repair(root)

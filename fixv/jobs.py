import re
from pathlib import Path
from typing import Optional

from .log import logger

BIN_DIR = 'Scripts'
ACT = 'activate.bat'

PATTERN = 'VIRTUAL_ENV=(.+?)(?=")'
ESC_RE = ('\\', '.', '+', '^', '$', '[', ']')  # may not enough


def _check_venv(root: Path):
    return (root / 'pyvenv.cfg').exists() and (root / BIN_DIR).exists()


def get_v_path(root: Path) -> Optional[str]:
    # assume `root` is valid
    act = root / BIN_DIR / ACT

    if not act.exists():
        return

    with open(act) as fp:
        line = fp.readline()
    logger.debug(f'GET: {line}')

    match = re.search(PATTERN, line)
    if match is None:
        return

    return match.group(1)


def _chk_and_fix(path: Path, pattern: bytes):
    with open(path, 'rb+') as fp:
        tmp = fp.read()

        match = re.search(pattern, tmp)
        if match is None:
            logger.debug(f'not match: {path}')
            return

        fp.seek(match.start())
        fp.write(bytes(path.parent.parent.absolute()))
        fp.write(tmp[match.end() :])

        logger.info(f'done: {path}')


def repair(root: Path):
    if not _check_venv(root):
        logger.error(f'invalid env: {root}')
        return

    match = get_v_path(root)
    logger.debug(f'{match=}')
    if match is None:
        logger.error(f'invalid env: {root}')
        return
    elif Path(match) == root.absolute():
        logger.info(f'OK env: {root}')
        return

    def pp(p: str) -> bytes:
        for esc in ESC_RE:
            p = p.replace(esc, f'\\{esc}')
        return p.encode()

    pattern = pp(match)
    for file in (root / BIN_DIR).glob('*'):
        _chk_and_fix(file, pattern)

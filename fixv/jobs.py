import re
from pathlib import Path
from typing import Optional

from .log import logger

PATTERN = 'VIRTUAL_ENV=(.+?)(?=")'
# re.compile(b'(?<=#!)(.+python)(?:\\.exe)?')
BIN_DIR = 'Scripts'  # Windows
ACT = 'activate.bat'


def _check_venv(root: Path):
    return (root / 'pyvenv.cfg').exists() and (root / BIN_DIR).exists()


def _get_v_path(root: Path) -> Optional[str]:
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


def _chk_and_fix(path: Path, pattern: str):
    def pp(p: str) -> bytes:
        return p.replace('\\', '\\\\').replace('.', '\\.').replace('+', '\\*').encode()

    with open(path, 'rb+') as fp:
        match = re.search(pp(pattern), fp.read())
        if match is None:
            logger.debug(f'not match: {path}')
            return

        fp.seek(match.end())
        end_bytes = fp.read()
        fp.seek(match.start())
        fp.write(bytes(path.parent.parent.absolute()))
        fp.write(end_bytes)

        logger.info(f'done: {path}')


def repair(root: Path):
    if not _check_venv(root):
        logger.error(f'invalid env: {root}')
        return

    match = _get_v_path(root)
    logger.debug(f'{match=}')
    if match is None:
        logger.error(f'invalid env: {root}')
        return
    elif Path(match) == root:
        logger.info(f'OK env: {root}')
        return

    for file in (root / BIN_DIR).glob('*'):
        _chk_and_fix(file, match)

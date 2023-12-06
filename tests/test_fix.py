import os
import sys

sys.path.insert(0, os.getcwd())

from pathlib import Path

from fixv.core import get_v_path, repair

INIT = Path('tests/env/x')
MOVE = Path('tests/env/z')


def test_init():
    assert INIT.exists()
    assert not MOVE.exists()

    vp = get_v_path(INIT)
    assert vp is not None
    assert Path(vp) == INIT.absolute()


def test_repair():
    INIT.rename(MOVE)
    assert not INIT.exists()
    assert MOVE.exists()

    repair(MOVE)
    vp = get_v_path(MOVE)
    assert vp is not None
    assert Path(vp) == MOVE.absolute()

    # reset
    MOVE.rename(INIT)
    assert not MOVE.exists()
    assert INIT.exists()

    repair(INIT)
    vp = get_v_path(INIT)
    assert vp is not None
    assert Path(vp) == INIT.absolute()

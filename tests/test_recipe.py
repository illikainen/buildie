from pytest import raises

from src.exceptions import BuildieExistError
from src.log import get_log

from .dummy import DefaultRecipe


def test_name_property(tmp_path):
    r = DefaultRecipe(
        log=get_log(), destdir=tmp_path, distfiles=tmp_path, workdir=tmp_path
    )
    assert r.name == "dummy"


def test_already_installed(tmp_path):
    with raises(BuildieExistError):
        (tmp_path / "dummy").mkdir()
        DefaultRecipe(
            log=get_log(),
            destdir=tmp_path,
            distfiles=tmp_path,
            workdir=tmp_path,
        )

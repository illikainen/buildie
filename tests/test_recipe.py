from pytest import raises

from src.exceptions import BuildieExistError, BuildieRecipeError
from src.log import get_log
from src.recipe import Recipe

from .dummy import DummyDefaultRecipe


def test_missing_name(tmp_path):
    with raises(BuildieRecipeError):
        Recipe(
            log=get_log(),
            destdir=tmp_path,
            distfiles=tmp_path,
            workdir=tmp_path,
        )


def test_already_installed(tmp_path):
    with raises(BuildieExistError):
        (tmp_path / DummyDefaultRecipe.name).mkdir()
        DummyDefaultRecipe(
            log=get_log(),
            destdir=tmp_path,
            distfiles=tmp_path,
            workdir=tmp_path,
        )

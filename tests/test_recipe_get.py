from pytest import raises

from src.exceptions import BuildieRecipeError
from src.recipe import Recipe, get_recipe


def test_missing_recipe():
    with raises(BuildieRecipeError):
        get_recipe("tests", "dummy1", "default")


def test_missing_variant():
    with raises(BuildieRecipeError):
        get_recipe("tests", "dummy", "default1")


def test_success():
    cls = get_recipe("tests", "dummy", "default")
    assert isinstance(Recipe, type(cls))

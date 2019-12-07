# pylint: disable=protected-access
from pytest import raises

from src.exceptions import BuildieVerifyError

from .utils import create_distfiles

failure = [
    ["truncated-sha256"],
    ["bogus-sha256"],
    ["empty-sha256"],
    ["missing-sha256"],
    ["truncated-sha256", "bogus-sha256", "empty-sha256"],
    ["truncated-sha256", "bogus-sha256", "valid-foo", "empty-sha256"],
    ["valid-foo", "truncated-sha256"],
    ["bogus-sha256", "valid-foo"],
]

success = [["valid-foo"], ["valid-foo", "valid-bar"]]


def test_failure(recipe, sources):
    for names in failure:
        create_distfiles(recipe, sources)

        recipe.sources = [sources[x] for x in names]
        with raises(BuildieVerifyError):
            recipe.verify()

        for name in names:
            assert not recipe._get_distfile(name).exists()
        assert not recipe._distfiles.exists()


def test_success(recipe, sources):
    for names in success:
        create_distfiles(recipe, sources)

        recipe.sources = [sources[x] for x in names]
        recipe.verify()

        for name in names:
            assert recipe._get_distfile(name).exists()
        assert recipe._distfiles.exists()

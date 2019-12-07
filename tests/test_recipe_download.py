# pylint: disable=protected-access
from unittest.mock import patch

from pytest import raises

from src.exceptions import BuildieDownloadError

from .utils import URLMock

exc = OSError(1, "foo", "bar", "baz")

failure = [
    [("valid-foo", exc)],
    [("valid-foo", None), ("valid-bar", exc)],
    [("valid-foo", None), ("bogus-sha256", exc), ("valid-bar", None)],
]

success = [[("valid-foo", None)], [("valid-foo", None), ("valid-bar", None)]]


def test_failure(recipe, sources):
    for retvals in failure:
        with patch("src.recipe.urlopen") as mock:
            mock.return_value = URLMock(retvals)

            recipe.sources = [sources[x] for x, _ in retvals]
            recipe.cleanup()
            recipe.prepare()
            with raises(BuildieDownloadError):
                recipe.download()

            for name, _ in retvals:
                assert not recipe._get_distfile(name).exists()
            assert not recipe._distfiles.exists()


def test_success(recipe, sources):
    for retvals in success:
        with patch("src.recipe.urlopen") as mock:
            mock.return_value = URLMock(retvals)

            recipe.sources = [sources[x] for x, _ in retvals]
            recipe.cleanup()
            recipe.prepare()
            recipe.download()

            for name, _ in retvals:
                assert recipe._get_distfile(name).exists()
            assert recipe._distfiles.exists()

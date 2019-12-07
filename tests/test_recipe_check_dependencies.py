from unittest.mock import patch

from pytest import raises

from src.exceptions import BuildieDependencyError

try:
    import apt

    HAVE_APT = True
except ImportError:
    HAVE_APT = False


def test_invalid_apt_package(recipe):
    if HAVE_APT:
        recipe.apt_dependencies = ["invalid-package-name"]
        with raises(BuildieDependencyError):
            recipe.check_dependencies()


def test_missing_apt_package(recipe):
    if HAVE_APT:
        pkg = None
        cache = apt.Cache()
        for pkg in cache:
            if not pkg.is_installed:
                break
        recipe.apt_dependencies = [pkg]
        with raises(BuildieDependencyError):
            recipe.check_dependencies()


def test_have_apt_package(recipe):
    if HAVE_APT:
        pkg = None
        cache = apt.Cache()
        for pkg in cache:
            if pkg.is_installed:
                break
        recipe.apt_dependencies = [pkg]
        recipe.check_dependencies()


def test_not_debian(recipe):
    with patch("src.recipe.is_debian") as mock:
        mock.return_value = False
        recipe.apt_dependencies = ["invalid-package-name"]
        recipe.check_dependencies()

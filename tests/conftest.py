from pytest import fixture

from src.log import get_log
from src.recipe import Source

from .dummy import DefaultRecipe


@fixture
def sources():
    return {
        "valid-foo": Source(
            url="valid-foo",
            path="valid-foo",
            sha256="4c3a76a82b3761dd46dd012fa3480"
            "e58fb5c51bca9793a3f73f0740d99524dc4",
        ),
        "valid-bar": Source(
            url="valid-bar",
            path="valid-bar",
            sha256="cbe25d84f1f92b33620613c4a9fd8"
            "121d05171800ca68f17d72a81c04a9d7e3f",
        ),
        "truncated-sha256": Source(
            url="truncated-sha256",
            path="truncated-sha256",
            sha256="c78c21a57428b0d3491b36df9b110"
            "f6c07d6af8dda153c664fde1322b88630d",
        ),
        "bogus-sha256": Source(
            url="bogus-sha256", path="bogus-sha256", sha256="abcd"
        ),
        "empty-sha256": Source(
            url="empty-sha256", path="empty-sha256", sha256=""
        ),
        "missing-sha256": Source(
            url="missing-sha256", path="missing-sha256", sha256=None
        ),
    }


@fixture
def recipe(tmp_path):
    destdir = tmp_path / "destdir"
    distfiles = tmp_path / "distfiles"
    workdir = tmp_path / "workdir"

    destdir.mkdir()
    distfiles.mkdir()
    workdir.mkdir()

    r = DefaultRecipe(
        log=get_log(), destdir=destdir, distfiles=distfiles, workdir=workdir
    )
    return r

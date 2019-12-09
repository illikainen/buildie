from shutil import copytree

from ...recipe import Recipe, Source
from ...utils import call, chdir, nproc


class DefaultRecipe(Recipe):
    """
    Fingerprint: 7A18 807F 100A 4570 C596  8420 7E4E 65C8 720B 706B
    """

    archive = "notmuch-0.29.3.tar.xz"
    mirror = "https://mirror.mdfnet.se/gentoo/distfiles"
    sources = [
        Source(
            url=f"{mirror}/{archive}",
            path=f"{archive}",
            sha256="d5f704b9a72395e43303de9b1f4d8e14"
            "dd27bf3646fdbb374bb3dbb7d150dc35",
        )
    ]
    apt_dependencies = [
        "build-essential",
        "libgmime-3.0-dev",
        "libtalloc-dev",
        "libxapian-dev",
        "pkg-config",
        "zlib1g-dev",
    ]

    def extract(self):
        with chdir(self._workdir):
            mu, *_ = self.sources
            distfile = self._get_distfile(mu.path)
            call("tar", "-xf", distfile, "--strip-components=1")

    def build(self):
        with chdir(self._workdir):
            call("./configure", f"--prefix={self._destdir}")
            call("make", "-j", nproc())
            copytree(
                self._workdir / "bindings" / "python" / "notmuch",
                self._destdir / "python" / "notmuch",
            )

    def install(self):
        with chdir(self._workdir):
            call("make", "install")

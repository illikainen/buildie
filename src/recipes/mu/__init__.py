from ...recipe import Recipe, Source
from ...utils import call, chdir, nproc


class MuDefaultRecipe(Recipe):
    variant = "default"
    name = "mu"
    archive = "mu-1.2.0.tar.xz"
    mirror = "https://ftp.openbsd.org/pub/OpenBSD/distfiles"
    sources = [
        Source(
            url=f"{mirror}/{archive}",
            path=f"{archive}",
            sha256="f634c7f244dc6844ff71dc3c3e1893e4"
            "8e193caa9e0e747eba616309775f053a",
        )
    ]
    apt_dependencies = [
        "build-essential",
        "libglib2.0-dev",
        "libgmime-3.0-dev",
        "libjson-glib-dev",
        "libxapian-dev",
        "pkg-config",
    ]

    def extract(self):
        with chdir(self._workdir):
            mu, *_ = self.sources
            distfile = self._get_distfile(mu.path)
            call("tar", "-xf", distfile, "--strip-components=1")

    def build(self):
        with chdir(self._workdir):
            call("./configure", "--prefix", self._destdir)
            call("make", "-j", nproc())

    def install(self):
        with chdir(self._workdir):
            call("make", "install")

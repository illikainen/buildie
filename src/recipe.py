from dataclasses import dataclass
from hashlib import sha256
from importlib import import_module
from os import environ
from pathlib import Path
from shutil import rmtree
from ssl import SSLError
from typing import List, Union
from urllib.request import urlopen

from .exceptions import (
    BuildieDependencyError,
    BuildieDownloadError,
    BuildieExistError,
    BuildieRecipeError,
    BuildieVerifyError,
)
from .utils import is_debian, read_fh


@dataclass
class Source:
    url: str
    path: Union[str, Path]
    sha256: str


class Recipe:
    sources: List[Source] = []
    apt_dependencies: List[str] = []
    cflags: List[str] = [
        "-D_FORTIFY_SOURCE=2",
        "-Werror=format-security",
        "-Wformat",
        "-Wformat-security",
        "-Wl,-z,now",
        "-Wl,-z,relro",
        "-fPIE",
        "-fstack-protector-all",
        "-pie",
    ]
    cxxflags: List[str] = cflags

    def __init__(self, log, destdir, distfiles, workdir):
        self._log = log
        self._destdir = destdir / self.name
        self._workdir = workdir / self.name
        self._distfiles = distfiles / self.name

        if self._destdir.exists():
            raise BuildieExistError(f"{self.name} is already installed")

    def run(self):
        self.cleanup()
        self.prepare()
        self.check_dependencies()
        self.download()
        self.verify()
        self.extract()
        self.build()
        self.test()
        self.install()
        self.cleanup()

    def cleanup(self):
        if self._workdir.exists():
            rmtree(self._workdir)

    def prepare(self):
        environ["CFLAGS"] = " ".join(self.cflags)
        environ["CXXFLAGS"] = " ".join(self.cxxflags)

        self._workdir.mkdir(parents=True, exist_ok=False)
        self._distfiles.mkdir(parents=True, exist_ok=True)

    def check_dependencies(self):
        missing = 0
        if is_debian():
            try:
                import apt
            except ImportError:
                raise BuildieDependencyError("need python3-apt")

            cache = apt.Cache()
            for dep in self.apt_dependencies:
                try:
                    pkg = cache[dep]
                except KeyError:
                    raise BuildieDependencyError(f"invalid dependency: {dep}")
                if not pkg.is_installed:
                    self._log.error(f"missing dependency: {dep}")
                    missing += 1

        if missing:
            raise BuildieDependencyError(f"missing {missing} dependencies")

    def download(self):
        for src in self.sources:
            path = self._get_distfile(src.path)
            if path.exists():
                self._log.info(f"already have {path.name}")
                continue

            self._log.info(f"download {path.name}")
            try:
                with urlopen(src.url) as req:
                    with path.open("wb") as f:
                        read_fh(req, f.write)
            except (OSError, SSLError) as e:
                rmtree(self._distfiles)
                raise BuildieDownloadError(
                    f"failed to download {src.url}: {e.filename}: {e.strerror}"
                )

    def verify(self):
        failures = 0
        for src in self.sources:
            path = self._get_distfile(src.path)
            self._log.info(f"verify {path.name}")

            digest = sha256()
            with path.open("rb") as f:
                read_fh(f, digest.update)

            if digest.hexdigest() == src.sha256:
                self._log.info(
                    f"successfully verified {path.name} ({src.sha256})"
                )
            else:
                self._log.error(f"failed to verify {path.name}")
                failures += 1

        if failures:
            rmtree(self._distfiles)
            raise BuildieVerifyError(f"failed to verify {failures} sources")

    def extract(self):
        pass

    def build(self):
        pass

    def test(self):
        pass

    def install(self):
        pass

    def _get_distfile(self, path):
        return self._distfiles / path

    @property
    def name(self):
        return type(self).__module__.split(".")[-1]


def get_recipe(path, name, variant):
    try:
        module = import_module(f"{path}.{name}")
    except ImportError:
        raise BuildieRecipeError(f"{name} is not a valid recipe")

    try:
        recipe = variant[0].upper() + variant[1:].lower() + "Recipe"
        return getattr(module, recipe)
    except AttributeError:
        raise BuildieRecipeError(f"{name} has no variant '{variant}'")

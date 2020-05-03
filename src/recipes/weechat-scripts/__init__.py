from shutil import copytree

from ...recipe import Recipe, Source
from ...utils import chdir


mirror = (
    "https://github.com/weechat/scripts/raw/"
    "183d51e457ecb5556926ed79ababb245aa161ba0"
)

autosort = Source(
    url=f"{mirror}/python/autosort.py",
    path="autosort.py",
    sha256="d90077f36afcd9497fbe214f7d7e2af20e1f46cbdfe50cd5cc73884b1ff0a644",
)

buffer_autohide = Source(
    url=f"{mirror}/python/buffer_autohide.py",
    path="buffer_autohide.py",
    sha256="5edd655bbf66295253bef5a6bdb999d51de9961185599021d721d35d0d4025ae",
)

go = Source(
    url=f"{mirror}/python/go.py",
    path="go.py",
    sha256="8dd62250f18195c308a59f665242e7745be67c108ab7f5256012d33f5f0bfe7d",
)

lnotify = Source(
    url=f"{mirror}/python/lnotify.py",
    path="lnotify.py",
    sha256="b92797b1f845d3a6185795ab60fb646f9f6d37540e178abcc084a49a13febc64",
)

urlgrab = Source(
    url=f"{mirror}/python/urlgrab.py",
    path="urlgrab.py",
    sha256="87479538ee0cb43a7b8a288d721f1bdcdba432c9f55059bcd2f8f092cf0324fd",
)


class DefaultRecipe(Recipe):
    sources = [autosort, buffer_autohide, go, lnotify, urlgrab]
    apt_dependencies = ["python3-weechat", "weechat"]

    def install(self):
        with chdir(self._workdir):
            for src in self.sources:
                copytree(src.path, self._destdir)

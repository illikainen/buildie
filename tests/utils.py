# pylint: disable=protected-access
from io import BytesIO


class URLMock:
    def __init__(self, retvals):
        self._retvals = retvals
        self._idx = 0

    def __enter__(self):
        rv, side_effect = self._retvals[self._idx]
        self._idx += 1

        if isinstance(side_effect, Exception):
            raise side_effect
        return BytesIO(rv.encode())

    def __exit__(self, *_args):
        pass


def create_distfiles(recipe, sources):
    for name, src in sources.items():
        path = recipe._get_distfile(src.path)
        path.parent.mkdir(exist_ok=True)
        path.write_text(name)

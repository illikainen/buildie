import logging

from . import __project__

INFO = logging.INFO
NONE = logging.CRITICAL + 1


def get_log(extra="", level=NONE):
    fmt = f"{extra} %(levelname)s: %(message)s"
    logging.basicConfig(format=fmt, level=level)
    log = logging.getLogger(__project__)
    return log

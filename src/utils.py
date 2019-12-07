import os
import sys
from contextlib import contextmanager
from multiprocessing import cpu_count
from pathlib import Path
from subprocess import PIPE, STDOUT, Popen

from .exceptions import BuildieCommandError


def is_debian():
    return Path("/etc/debian_version").exists()


def call(*args, show=True):
    cmd = [str(x) for x in args]
    stdout = []
    try:
        p = Popen(cmd, stdout=PIPE, stderr=STDOUT)
        for line in iter(p.stdout.readline, b""):
            sline = line.decode()
            if show:
                sys.stdout.write(sline)
            stdout.append(sline)
        p.wait()
    except OSError as e:
        raise BuildieCommandError(f"{' '.join(cmd)}: {e.strerror}")
    if p.returncode:
        raise BuildieCommandError(f"{' '.join(cmd)}: {' '.join(stdout)}")
    return "".join(stdout)


def read_fh(f, callback):
    while True:
        chunk = f.read(4096)
        if not chunk:
            break
        callback(chunk)


def nproc():
    return cpu_count()


@contextmanager
def chdir(path):
    old = os.getcwd()
    os.chdir(path)
    yield
    os.chdir(old)

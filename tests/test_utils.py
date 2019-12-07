import os
from unittest.mock import patch

from pytest import raises

from src.exceptions import BuildieCommandError
from src.utils import call, chdir, nproc


def test_call_rv_success(tmp_path):
    (tmp_path / "foo").touch()
    assert call("ls", tmp_path, show=False) == "foo\n"


def test_call_rv_failure(tmp_path):
    with raises(BuildieCommandError) as e:
        call("ls", tmp_path / "foo")
    assert "No such file or directory" in str(e)


def test_call_command_failure():
    with raises(BuildieCommandError):
        call("ls1234")


def test_nproc():
    with patch("src.utils.cpu_count") as mock:
        mock.return_value = 555
        assert nproc() == 555


def test_chdir(tmp_path):
    old = os.getcwd()
    with chdir(tmp_path):
        assert os.getcwd() == str(tmp_path)
    assert os.getcwd() == old

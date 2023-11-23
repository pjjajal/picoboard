# Copyright (c) 2023 Purvish Jajal
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os

import pytest

from picoboard import PicoLogger


@pytest.fixture
def picologger(tmpdir):
    return PicoLogger(log_dir=tmpdir)


def test_log_exists(picologger):
    assert os.path.exists(picologger.log_path)


def test_logging(picologger):
    picologger.log_scalar("val_acc", "0.22")
    with open(picologger.log_path, "r") as f:
        logged_message = f.read()

    assert "VAL_ACC: 0.22" in logged_message


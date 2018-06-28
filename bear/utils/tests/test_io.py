# -*- coding: utf-8 -*-

from __future__ import absolute_import

from bear import package_location
from bear.utils.io import copy_to, read_write

import os
from os.path import join

loc = package_location()


def test_copy():
    copy_to_loc = "./"
    file_location = join(loc, "templates", "build_tools",
                         "travis", "after_success.txt")

    assert os.path.exists(loc)
    try:
        copy_to(file_location, copy_to_loc, verbose=False)
        assert os.path.exists("./after_success.txt")
    finally:
        if os.path.exists("./after_success.txt"):
            os.unlink("./after_success.txt")


def test_read_write():
    pass

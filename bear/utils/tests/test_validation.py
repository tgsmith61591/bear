# -*- coding: utf-8 -*-

from __future__ import absolute_import

from bear.utils.validation import (validate_path,
                                   validate_project_name,
                                   validate_requirements)

import pytest
import shutil
import six
import os


def test_validate_path():
    # Validate we get/set the path right
    name = "name"
    assert validate_path("", name) == "./name"
    assert validate_path("./name", "name") == "./name"

    # show this will fail
    try:
        # make a directory
        os.mkdir(name)
        with pytest.raises(OSError):
            validate_path("", name)

    finally:
        shutil.rmtree(name)

    assert not os.path.exists(name)


def test_validate_project_name():
    def assert_bad_name(name):
        with pytest.raises(ValueError):
            validate_project_name(name)

    assert_bad_name(None)
    assert_bad_name("")
    assert_bad_name("bad\nname")
    assert_bad_name("bad" + os.sep + "name")
    assert_bad_name("..")
    assert_bad_name(".")

    assert validate_project_name("GoodName") == "GoodName"


def test_validate_requirements():
    # Test for None first
    req = validate_requirements(None, False)
    assert isinstance(req, six.string_types), type(req)
    assert req == "numpy>=1.12", req

    # Test for existing reqs
    req = validate_requirements("a>=1, g, b<3", True)
    assert "numpy>=1.12" in req
    assert sorted(req.split()) == \
           ['a>=1', 'b<3', 'cython>=0.23', 'g', 'numpy>=1.12'], req.split()

# -*- coding: utf-8 -*-

from __future__ import absolute_import

from bear.defaults import default_values
from bear.utils.yaml import parse_yaml
from bear.utils.validation import validate_args
from bear.utils.testing import SimulatedNamespace, with_temporary_file

import pytest

# We'll use the same file for all tests
config_file = "test_config.yml"
create_defaults = default_values["create"]


def test_parse_non_existent():
    with pytest.raises(OSError):
        parse_yaml("non-existent", create_defaults)


@with_temporary_file(config_file, """
project_name: test_package
""")
def test_parse_passing_yaml():
    parsed = parse_yaml(config_file, create_defaults)
    assert parsed['project_name'] == 'test_package'

    # show it will pass
    validate_args(SimulatedNamespace(**parsed))


@with_temporary_file(config_file, """
git_user: tgsmith61591
""")
def test_parse_failing_yaml():
    parsed = parse_yaml(config_file, create_defaults)
    assert parsed['git_user'] == "tgsmith61591"

    # show it fails since the project_name is not specified
    with pytest.raises(ValueError):
        validate_args(SimulatedNamespace(**parsed))


@with_temporary_file(config_file, """
project_name: test_package
circle: true
""")
def test_store_true_value():
    parsed = parse_yaml(config_file, create_defaults)

    # Show that the stored value of "circle" is True (the bool)
    assert parsed['circle'] is True
    assert parsed['travis'] is False

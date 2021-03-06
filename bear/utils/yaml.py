# -*- coding: utf-8 -*-

from __future__ import absolute_import

import yaml
import os
import six

__all__ = ['parse_yaml']


def parse_yaml(path, defaults):
    """Parse the arguments from a YAML file.

    Parameters
    ----------
    path : str or unicode
        A path to the YAML config file.

    defaults : dict
        A dictionary of default arguments for the "create" method.
    """
    # The file must exist
    if not path or not os.path.exists(path):
        raise OSError("Config file (%s) does not exist!" % path)

    # Open it, read it and parse it
    with open(path, "r") as yml:
        contents = yml.read()
    parsed = yaml.load(contents)

    # If there are any keys in defaults that are not filled in parsed,
    # set them
    for k, v in six.iteritems(defaults):
        if k not in parsed:
            parsed[k] = v

    # For any of the "store_true" type values, we should have automatically
    # parsed the bool... i.e., true -> True. However, "true" will not yield
    # True, but "True" (the str). This is tested in bear/utils/tests/test_yaml

    return parsed

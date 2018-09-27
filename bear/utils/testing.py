# -*- coding: utf-8 -*-
#
# Testing utilities

from __future__ import absolute_import

import os
import six
from os.path import join
import shutil

from functools import wraps

__all__ = ['make_and_cleanup_project_path',
           'with_temporary_file',
           'SimulatedNamespace']


def make_and_cleanup_project_path(project_path, *subdirectories):
    r"""Manage the project-level directory for tests.

    Create the project-level directory before running the test,
    and then clean it up after the test. This is all managed within a
    try/finally so that the tests don't have to handle the pattern.

    Parameters
    ----------
    project_path : str or unicode
        The project-level directory for testing. This should not exist prior
        to the function call.

    *subdirectories : varargs
        The subdirectories to be created under ``project_path``.

    Notes
    -----
    Every file created should land inside of the ``project_path`` to ensure
    artifacts are properly cleaned up.
    """
    def func_wrapper(func):
        @wraps(func)
        def test_wrapper(*args, **kwargs):
            assert not os.path.exists(project_path)

            subdirs = [join(project_path, s) for s in subdirectories]
            for subdir in subdirs:
                assert not os.path.exists(subdir)

            try:
                os.mkdir(project_path)
                for subdir in subdirs:
                    os.mkdir(subdir)

                func(*args, **kwargs)
            finally:
                # Always remove the project path to make sure it's gone if we
                # failed somewhere along the way
                shutil.rmtree(project_path)
                assert not os.path.exists(project_path)
        return test_wrapper
    return func_wrapper


# Helper function to write yaml files
def _write_file(config_file, content):
    with open(config_file, 'w') as yml:
        yml.write(content)


def with_temporary_file(config_file, content):
    """Write and destroy a temporary file for configuration tests.

    Used to decorate a test that depends on a temporary (typically a YAML)
    file. Asserts the file does not exist, writes the file, executes the test
    and then destroys the file.

    Parameters
    ----------
    config_file : str or unicode
        The path where the configuration file should be written.

    content : str or unicode
        The content of the YAML file
    """
    def func_wrapper(func):
        def actual_wrapper(*args, **kwargs):
            assert not os.path.exists(config_file)
            try:
                _write_file(config_file, content)
                func(*args, **kwargs)
            finally:
                os.unlink(config_file)
        return actual_wrapper
    return func_wrapper


class SimulatedNamespace(object):
    # Simulate an Arguments Namespace object
    def __init__(self, **kwargs):
        for k, v in six.iteritems(kwargs):
            setattr(self, k, v)

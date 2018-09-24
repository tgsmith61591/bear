# -*- coding: utf-8 -*-
#
# Testing utilities

from __future__ import absolute_import

import os
import shutil

from functools import wraps

__all__ = ['make_and_cleanup_project_path']


def make_and_cleanup_project_path(project_path):
    """Manage the project-level directory for tests.

    Create the project-level directory before running the test,
    and then clean it up after the test. This is all managed within a
    try/finally so that the tests don't have to handle the pattern.

    Parameters
    ----------
    project_path : str or unicode
        The project-level directory for testing. This should not exist prior
        to the function call.

    Notes
    -----
    Every file created should land inside of the ``project_path`` to ensure
    artifacts are properly cleaned up.
    """
    def func_wrapper(func):
        @wraps(func)
        def test_wrapper(*args, **kwargs):
            assert not os.path.exists(project_path)
            try:
                os.mkdir(project_path)
                func(*args, **kwargs)
            finally:
                # Always remove the project path to make sure it's gone if we
                # failed somewhere along the way
                shutil.rmtree(project_path)
        return test_wrapper
    return func_wrapper

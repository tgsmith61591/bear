# -*- coding: utf-8 -*-

from __future__ import absolute_import

from bear.utils.testing import make_and_cleanup_project_path

import subprocess
from os.path import join, exists

project_path = "test_project_path"
package_name = "test_package_name"


def _run_cmd(args):
    proc = subprocess.Popen(args, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            shell=False)

    # Get the result
    strres = proc.communicate()
    print(strres)  # in case we fail, it will be in pytest log
    return proc.returncode


@make_and_cleanup_project_path(project_path=project_path)
def test_bear_create():
    args = ["python", "-m", "bear", "create",
            "--path", project_path,
            "--name", package_name]

    # Create the package, assert it's there
    result_code = _run_cmd(args)
    assert result_code == 0, result_code

    # Now assert that things were properly created
    assert exists(project_path)
    assert exists(join(project_path, package_name))


# Show we fail without a specified package name
@make_and_cleanup_project_path(project_path=project_path)
def test_bear_create_fail():
    args = ["python", "-m", "bear", "create",
            "--path", project_path]

    result_code = _run_cmd(args)
    assert result_code != 0, result_code

    # The project package path should not exist since we failed
    assert not exists(join(project_path, package_name))


# TODO: yaml file tests

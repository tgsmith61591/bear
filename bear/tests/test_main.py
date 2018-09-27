# -*- coding: utf-8 -*-

from __future__ import absolute_import

from bear.utils.testing import make_and_cleanup_project_path, \
    with_temporary_file

import subprocess
from os.path import join, exists

config_file = "test_config.yml"
project_path = "test_project_path"
package_name = "test_package_name"


def _run_cmd(args):
    proc = subprocess.Popen(args, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            shell=False)

    # Get the result
    strres = proc.communicate()
    return strres, proc.returncode


@make_and_cleanup_project_path(project_path=project_path)
def test_bear_create():
    args = ["python", "-m", "bear", "create",
            "--path", project_path,
            "--project_name", package_name]

    # Create the package, assert it's there
    strres, result_code = _run_cmd(args)
    assert result_code == 0, strres[1]

    # Now assert that things were properly created
    assert exists(join(project_path, package_name))


# Show we fail without a specified package name
@make_and_cleanup_project_path(project_path=project_path)
def test_bear_create_fail():
    args = ["python", "-m", "bear", "create",
            "--path", project_path]

    strres, result_code = _run_cmd(args)
    assert result_code != 0, strres[1]

    # The project package path should not exist since we failed
    assert not exists(join(project_path, package_name))


@make_and_cleanup_project_path(project_path=project_path)
@with_temporary_file(config_file, """
path: test_project_path
project_name: test_package_name
git_user: tgsmith61591
travis: true
""")
def test_bear_yaml_travis_no_circle():
    args = ["python", "-m", "bear", "yaml",
            "--file", config_file]

    strres, result_code = _run_cmd(args)
    assert result_code == 0, strres[1]

    # The package should exist
    assert exists(join(project_path, package_name))

    # as should the "travis" files
    build_tools = join(project_path, package_name, "build_tools")
    assert exists(join(build_tools, "travis"))
    assert not exists(join(build_tools, "circle"))


def test_unknown_args():
    args = ["python", "-m", "bear", "create",
            "--project_name", package_name,
            "--file", config_file]

    # Should fail since we mixed args
    strres, result_code = _run_cmd(args)
    assert result_code != 0, (strres, result_code)

# -*- coding: utf-8 -*-

from __future__ import absolute_import

from bear.utils.testing import make_and_cleanup_project_path
import subprocess

project_path = "test_project_path"
package_name = "test_package_name"


@make_and_cleanup_project_path(project_path=project_path)
def test_bear_create():
    args = ["python", "-m", "bear", "create",
            "--path", project_path,
            "--name", package_name]

    # Create the package, assert it's there
    

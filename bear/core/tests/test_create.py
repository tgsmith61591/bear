# -*- coding: utf-8 -*-

from __future__ import absolute_import

import bear
from bear.utils.testing import make_and_cleanup_project_path
from bear.utils.validation import validate_requirements
from bear.core.create import make_package, _create_project_level, \
    _create_package_level, _create_examples_dir, _create_ci_build_tools

import os
from os.path import join
import shutil

# Attrs of the bear package
bear_location = bear.package_location()
bear_version = bear.__version__

# Template directories
templates = join(bear_location, "templates")
project_level_templates = join(templates, "project_level")
pkg_level_templates = join(templates, "package_level")
example_level_templates = join(templates, "examples")
doc_level_templates = join(templates, "doc")
ci_level_templates = join(templates, "build_tools")

# Attrs of the TEST package we want to create
project_path = "bear_test_project_dir"
package_name = "bear_test"
path = join(project_path, package_name)
author = "Fake Authorman"
email = "some_email@fake.com"
python = "3.5"
git_user = "fakegituser"
license = "MIT"

# Requirements
requirements_no_c = validate_requirements(None, False)
requirements_with_c = validate_requirements(None, True)

# Simple header we'll use
header = """# -*- coding: utf-8 -*-
# Auto-generated with bear v%s, (c) Taylor G Smith
""" % bear_version


@make_and_cleanup_project_path(project_path=project_path)
def test_create_project_level_no_c():
    # Operate as if the project dir exists, since decorator should handle it.
    _create_project_level(proj_level=project_level_templates,
                          path=path, verbose=True,
                          name=package_name, bear_version=bear_version,
                          description="A bear test package!",
                          requirements=requirements_no_c,
                          header=header, author=author, email=email,
                          python=python, c=False, git_user=git_user,
                          license=license)

    # Now assert the files in interest exist


def test_create_project_level_with_c():
    pass


def test_create_package_level():
    pass


def test_create_examples_dir():
    pass


def test_create_ci_build_tools():
    pass


def test_make_package():
    pass

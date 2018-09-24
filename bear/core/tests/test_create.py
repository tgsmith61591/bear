# -*- coding: utf-8 -*-

from __future__ import absolute_import

import bear
from bear.utils.testing import make_and_cleanup_project_path
from bear.utils.validation import validate_requirements
from bear.core.create import make_package, _create_project_level, \
    _create_package_level, _create_examples_dir, _create_ci_build_tools

import os
from os.path import join

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
lic = "MIT"

# Simple header we'll use
header = """# -*- coding: utf-8 -*-
# Auto-generated with bear v%s, (c) Taylor G Smith
""" % bear_version


def _project_assertions(c):
    # Now assert the files in interest exist
    for filename in ('.coveragerc', '.gitignore', '.travis.yml',
                     'LICENSE', 'MANIFEST.in', 'README.md',
                     'requirements.txt', 'setup.py'):
        assert os.path.exists(join(path, filename))

    # The requirements should NOT have cython
    proj_dir = join(project_path, package_name)
    with open(join(proj_dir, 'requirements.txt'),
              'r') as reqs:
        require = reqs.read().lower()
        assert 'numpy' in require

        # This is really the only piece that changes depending on C
        if c:
            assert 'cython' in require
        else:
            assert 'cython' not in require

    # Show we correctly write the .coveragerc
    with open(join(proj_dir, '.coveragerc'), 'r') as cov:
        coverage = cov.read().lower()
        assert '*/{package_name}/setup.py'.format(
            package_name=package_name) in coverage


@make_and_cleanup_project_path(project_path, package_name)
def create_project_level(c):
    # Operate as if the project dir exists, since decorator should handle it.
    _create_project_level(proj_level=project_level_templates,
                          path=path, verbose=True,
                          name=package_name, bear_version=bear_version,
                          description="A bear test package!",
                          requirements=validate_requirements(None, c),
                          header=header, author=author, email=email,
                          python=python, c=c, git_user=git_user,
                          license=lic)

    # Modularize this so we can assert them from other areas as well
    _project_assertions(c)

    # The package itself should NOT exist in there yet
    proj_dir = join(project_path, package_name)
    assert not os.path.exists(join(proj_dir, package_name))


# Runs the above function TWICE
def test_project_level_code():
    for c in (True, False):
        create_project_level(c)


def _package_assertions(c):
    # First, show the package level DOES exist
    proj_level = join(project_path, package_name)
    package_level = join(proj_level, package_name)
    assert os.path.exists(package_level)

    # these will always (should always) be there
    assert os.path.exists(join(package_level, '__init__.py'))
    assert os.path.exists(join(package_level, 'setup.py'))

    # If c was required, we should have a __check_build and more...
    if c:
        assert os.path.exists(join(package_level, '__check_build'))
        assert os.path.exists(join(package_level, '_build_utils'))

    # If C, the __init__ will contain more
    c_import = "from . import __check_build"
    with open(join(package_level, '__init__.py'), 'r') as init:
        _init = init.read()
        if c:
            assert c_import in _init
        else:
            assert c_import not in _init

    # Same with the setup.py
    with open(join(package_level, 'setup.py'), 'r') as stp:
        setup = stp.read()

        # For C, we expect the lines to be uncommented
        uncommented_str = "config.add_subpackage('__check_build')"
        commented_str = "# %s" % uncommented_str

        # For no C, we expect this to be commented
        if not c:
            assert commented_str in setup
        else:
            assert commented_str not in setup and uncommented_str in setup


@make_and_cleanup_project_path(project_path, package_name)
def create_package_level(c):
    _create_package_level(package_templates=pkg_level_templates,
                          path=path, c=c, version=bear_version,
                          verbose=True, name=package_name,
                          header=header)

    _package_assertions(c)


def test_package_level_code():
    for c in (True, False):
        create_package_level(c)


def test_create_examples_dir():
    pass


def test_create_ci_build_tools():
    pass


# For this one, we'll just embed the package/project assertions, etc.
@make_and_cleanup_project_path(project_path)
def do_make_package(c):
    make_package(header=header, bear_location=bear_location,
                 bear_version=bear_version, author=author,
                 description="Test project", email=email,
                 git_user=git_user, license=lic,
                 name=package_name, path=path,
                 python=python, requirements=validate_requirements(None, c),
                 version=bear_version, c=c, verbose=True)

    # Co-op the other assertion functions
    _project_assertions(c)
    _package_assertions(c)


def test_make_package():
    for c in (True, False):
        do_make_package(c)

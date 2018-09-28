# -*- coding: utf-8 -*-

from __future__ import absolute_import

import bear
from bear.utils.testing import make_and_cleanup_project_path
from bear.utils.validation import validate_requirements
from bear.core.create import make_package, _create_project_level, \
    _create_package_level, _create_examples_dir, _create_ci_build_tools, \
    _create_doc

import datetime
import pytest
import os
from os.path import join

# Attrs of the bear package
bear_location = bear.package_location()
bear_version = bear.__version__
year = str(datetime.datetime.now().year)

# Template directories
templates = join(bear_location, "templates")
project_level_templates = join(templates, "project_level")
pkg_level_templates = join(templates, "package_level")
example_level_templates = join(templates, "examples")
doc_level_templates = join(project_level_templates, "doc")
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
description="This is a test pkg"

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
                          license=lic, year=year)

    # Modularize this so we can assert them from other areas as well
    _project_assertions(c)

    # The package itself should NOT exist in there yet
    proj_dir = join(project_path, package_name)
    assert not os.path.exists(join(proj_dir, package_name))


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


def _examples_assertions(c):
    # There's not much to assert here since it relies on the user to fill it
    # in... but we can make minor assertions
    examples_directory = join(project_path, package_name, "examples")
    with open(join(examples_directory, "README.txt")) as rdme:
        script = rdme.read()
        assert "submodules in {package_name}".format(
            package_name=package_name) in script


@make_and_cleanup_project_path(project_path, package_name)
def create_examples_level(c):
    _create_examples_dir(examples_templates=example_level_templates,
                         path=path, verbose=True, name=package_name)
    _examples_assertions(c)


def _travis_assertions(c):
    build_tools = join(project_path, package_name, "build_tools")
    travis_path = join(build_tools, "travis")

    # Now Travis, which is a bit more convoluted
    for f in ('after_success.sh', 'before_install.sh', 'before_script.sh',
              'build_manywheels_linux.sh', 'build_wheels.sh', 'install.sh',
              'setup.cfg', 'test_script.sh'):
        assert os.path.exists(join(travis_path, f))

    # Assert on some of the write outputs
    with open(join(travis_path, 'after_success.sh')) as aftersuccess:
        script = aftersuccess.read()
        assert "rm -r {package_name}.egg-info/".format(
            package_name=package_name) in script

    # Assert that C is or is not required in some scripts
    for f in ("before_install.sh", "install.sh"):
        with open(join(travis_path, f)) as installscript:
            script = installscript.read()
            if c:
                assert '"true" == "true"' in script
            else:
                assert '"false" == "true"' in script


def _circle_assertions(c):
    build_tools = join(project_path, package_name, "build_tools")
    circle_path = join(build_tools, "circle")

    # assert that the build_test_pypy.sh file exists and that
    # the package name was appropriately written in
    assert os.path.exists(join(circle_path, "build_test_pypy.sh"))
    with open(join(circle_path, "build_test_pypy.sh"), "r") as pypy_sh:
        script = pypy_sh.read()
        assert "python -m pytest {package_name}/".format(
            package_name=package_name) in script, script

        # If C, assert cython is in there
        if c:
            assert "Cython" in script
        else:
            assert "Cython" not in script


def _ci_assertions(c):
    _circle_assertions(c)
    _travis_assertions(c)


@make_and_cleanup_project_path(project_path, package_name)
def create_ci_both_true(c):
    _create_ci_build_tools(ci_templates=ci_level_templates, path=path,
                           name=package_name, verbose=True, c=c,
                           proj_level=project_level_templates,
                           travis=True, circle=True)
    _ci_assertions(c)


@make_and_cleanup_project_path(project_path, package_name)
def create_ci_only_travis(c):
    _create_ci_build_tools(ci_templates=ci_level_templates, path=path,
                           name=package_name, verbose=True, c=c,
                           proj_level=project_level_templates,
                           travis=True, circle=False)
    _travis_assertions(c)


@make_and_cleanup_project_path(project_path, package_name)
def create_ci_only_circle(c):
    _create_ci_build_tools(ci_templates=ci_level_templates, path=path,
                           name=package_name, verbose=True, c=c,
                           proj_level=project_level_templates,
                           travis=False, circle=True)
    _circle_assertions(c)


def _doc_assertions(c):
    # First, assert the doc folder even exists
    doc_dir = join(project_path, package_name, "doc")
    assert os.path.exists(doc_dir)

    # Show each of the subdirs exist
    subdirs = (join("_static", "css"), "_templates", "includes", "modules",
               "sphinxext")
    for subdir in subdirs:
        assert os.path.exists(join(doc_dir, subdir))

    # Read the config and show the package name exists as expected
    with open(join(doc_dir, "conf.py"), 'r') as cfg:
        conf = cfg.read()

    assert package_name in conf
    assert author in conf
    assert year in conf


@make_and_cleanup_project_path(project_path, package_name)
def create_documentation(c):
    _create_doc(doc_templates=doc_level_templates, path=path, name=package_name,
                requirements=validate_requirements(None, c), verbose=True,
                bear_version=bear_version, description=description,
                author=author, year=year, git_user=git_user)

    _doc_assertions(c)


# For this one, we'll just embed the package/project assertions, etc.
@make_and_cleanup_project_path(project_path)
def do_make_package(c):
    make_package(header=header, bear_location=bear_location,
                 bear_version=bear_version, author=author,
                 description="Test project", email=email,
                 git_user=git_user, license=lic,
                 name=package_name, path=path,
                 python=python, requirements=validate_requirements(None, c),
                 version=bear_version, c=c, verbose=True,
                 travis=True, circle=True)

    # Co-op the other assertion functions
    _project_assertions(c)
    _package_assertions(c)
    _ci_assertions(c)
    _examples_assertions(c)
    _doc_assertions(c)


# This is really the test runner grid. Runs each create function with
# a different value of C (True or False)
@pytest.mark.parametrize('func', [
    create_project_level,
    create_package_level,
    create_examples_level,
    create_ci_both_true,
    create_ci_only_travis,
    create_ci_only_circle,
    create_documentation,
    do_make_package
])
def test_respective_create_functions(func):
    for c in (True, False):
        func(c)

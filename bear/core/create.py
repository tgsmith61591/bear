# -*- coding: utf-8 -*-

from __future__ import absolute_import

from ..utils.io import read_write, copy_to

import os
from os.path import join
import datetime

__all__ = ['make_package']


def _create_project_level(proj_level, path, verbose, name, bear_version,
                          description, requirements, header, author, email,
                          python, c, git_user, license):
    """Create the top-level of the project (not the package)"""
    # NOTE:
    # proj_level : The project-level TEMPLATE directory
    # path : The TARGET path for the project

    # This is the coverage configuration
    read_write(join(proj_level, ".coveragerc"), write_to_dir=path,
               suffix=None, verbose=verbose, package_name=name)

    # This is the gitignore file
    read_write(join(proj_level, ".gitignore"), write_to_dir=path,
               suffix=None, verbose=verbose)

    # The yml file to configure Travis CI/CD. You'll have to include your
    # own pypi credentials to deploy anything
    read_write(join(proj_level, ".travis.txt"), write_to_dir=path,
               suffix=".yml", verbose=verbose, package_name=name)

    # The MANIFEST for the project
    read_write(join(proj_level, "MANIFEST.txt"), write_to_dir=path,
               suffix=".in", verbose=verbose, package_name=name)

    # The README for the project
    read_write(join(proj_level, "README.txt"), write_to_dir=path,
               suffix=".md", verbose=verbose, package_name=name,
               bear_version=bear_version, description=description)

    # The requirements file
    read_write(join(proj_level, "requirements.txt"), write_to_dir=path,
               suffix=".txt", verbose=verbose, requirements=requirements)

    # The setup.py. If the description is empty, we need to put something there
    # so that the docstring at the top is not empty...
    read_write(join(proj_level, "setup.txt"), write_to_dir=path,
               suffix=".py", verbose=verbose, header=header, package_name=name,

               # Make sure the docstring in the head gets something...
               description=description if description else name,
               author=author, author_email=email, python_requires=python,
               c=str(c), license=license, git_username=git_user,
               package_name_upper=name.upper())

    # Now, move over the appropriate license
    read_write(join(proj_level, "licenses", license), write_to_dir=path,
               overwrite_name="LICENSE", verbose=verbose,
               package_name=name, year=str(datetime.datetime.now().year))


def _create_package_level():
    pass


def make_package(header, bear_location, bear_version,
                 author, description, email, git_user, license,
                 name, path, python, requirements, version, c, verbose):
    """Build the package.

    For each template file in bear/templates, read the file in plain text,
    format them with kwarg values and then write them into the new package
    with the approprite suffix.

    Parameters
    ----------
    header : str or unicode
        The header to place in created templates. Attributes the creation to
        Bear.

    bear_location : str or unicode
        The location of the Bear package on disk for finding templates.

    bear_version : str or unicode
        The version of Bear that created the package.

    author : str or unicode
        The author or the package. This is written in several places,
        including the new project's setup.py.

    description : str or unicode
        The description for the package. This is written into the new
        project's setup.py.

    email : str or unicode
        The author email. This is written into the project's setup.py to
        be searchable on pypi.

    git_user : str or unicode
        The git username of the author.

    license : str or unicode
        The name of the license to use for the package. This will be
        included in the setup.py

    name : str or unicode
        The name of the package

    path : str or unicode
        The absolute path to the location where the package will be created.

    python : str or unicode
        The required python version

    requirements : str or unicode
        The package requirements to be written in requirements.txt

    version : str or unicode
        The version of the package to build

    c : bool
        Whether C is required to build the package.

    verbose : bool
        Whether to build in verbose mode.
    """
    # Make the path for the project
    os.mkdir(path)

    # Project level
    templates = join(bear_location, "templates")
    proj_level = join(templates, "project_level")
    pkg_level = join(templates, "package_level")
    ex_level = join(templates, "examples")
    doc_level = join(templates, "doc")
    trav_level = join(templates, "build_tools", "travis")

    # Create the top level of the project (not the package yet)
    _create_project_level(proj_level=proj_level, path=path, verbose=verbose,
                          name=name, bear_version=bear_version,
                          description=description, requirements=requirements,
                          header=header, author=author, email=email,
                          python=python, c=c, git_user=git_user,
                          license=license)

    # Now create the package-level
    package = join(path, name)
    os.mkdir(package)
    read_write(join(pkg_level, "__init__.txt"), write_to_dir=package,
               suffix=".py", verbose=verbose, header=header,
               version=version, package_name_upper=name.upper(),
               package_name=name)

    # If we are using Cython, then we will not comment out the cythonization
    # lines. Otherwise we will.
    read_write(join(pkg_level, "setup.txt"), write_to_dir=package,
               suffix=".py", verbose=verbose, header=header,
               package_name=name,

               # Insert a comment in front of cython lines if not using cython
               comment_for_no_c="# " if not c else "")

    # If we're depending on building C code, we need to create the
    # __check_build and _build_utils submodules
    if c:
        cb_template = join(pkg_level, "__check_build")
        check_build = join(package, "__check_build")
        os.mkdir(check_build)

        read_write(join(cb_template, "__init__.txt"),
                   write_to_dir=check_build, suffix=".py",
                   verbose=verbose,
                   package_name=name)

        # For the files we just want to copy...
        for copyfile in ("_check_build.pyx", "setup.py"):
            copy_to(join(cb_template, copyfile),
                    write_to_dir=check_build,
                    verbose=verbose)

        # We also want the test directory
        cb_tests_template = join(cb_template, "tests")
        check_build_tests = join(check_build, "tests")
        os.mkdir(check_build_tests)

        # Move the __init__ file
        copy_to(join(cb_tests_template, "__init__.py"),
                write_to_dir=check_build_tests,
                verbose=verbose)

        # Format the test script itself and put it
        read_write(join(cb_tests_template, "test_check_build.txt"),
                   write_to_dir=check_build_tests, suffix=".py",
                   verbose=verbose,
                   package_name=name)

        # Now move over the _build_utils stuff
        bu_template = join(pkg_level, "_build_utils")
        build_utils = join(package, "_build_utils")
        os.mkdir(build_utils)

        read_write(join(bu_template, "__init__.txt"),
                   write_to_dir=build_utils, suffix=".py",
                   verbose=verbose,
                   package_name=name)

    # Create the examples directory
    examples = join(path, "examples")
    os.mkdir(examples)
    read_write(join(ex_level, "README.txt"), write_to_dir=examples,
               suffix=".txt", verbose=verbose, package_name=name)

    # Create the build_tools/travis components
    travis = join(path, "build_tools", "travis")
    os.makedirs(travis)  # recursive so it makes both dirs
    read_write(join(trav_level, "after_success.txt"), write_to_dir=travis,
               suffix=".sh", verbose=verbose, package_name=name)

    read_write(join(trav_level, "before_install.txt"), write_to_dir=travis,
               suffix=".sh", verbose=verbose, c="true" if c else "false")

    read_write(join(trav_level, "before_script.txt"), write_to_dir=travis,
               suffix=".sh", verbose=verbose)

    copy_to(join(trav_level, "build_manywheels_linux.sh"),
            write_to_dir=travis, verbose=verbose)

    copy_to(join(trav_level, "build_wheels.sh"),
            write_to_dir=travis, verbose=verbose)

    read_write(join(trav_level, "install.txt"), write_to_dir=travis,
               suffix='.sh', verbose=verbose, c="true" if c else "false")

    copy_to(join(trav_level, "setup.cfg"),
            write_to_dir=travis, verbose=verbose)

    read_write(join(trav_level, "test_script.txt"),
               write_to_dir=travis, suffix=".sh", verbose=verbose,
               package_name=name)

    # TODO: someday do the doc level

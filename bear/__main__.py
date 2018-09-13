# -*- coding: utf-8 -*-

from __future__ import absolute_import

import argparse
from argparse import RawTextHelpFormatter

import bear
from bear.utils.io import read_write, copy_to
from bear.utils.validation import validate_args

import shutil
import os
from os.path import join

# The bear version, used to build the README
bear_version = bear.__version__
bear_location = bear.package_location()

# The header we'll write to the top of all the python files
header = """# -*- coding: utf-8 -*-
# Auto-generated with bear v%s, (c) Taylor G Smith
""" % bear_version


def make_package(author, description, email, git_user, license,
                 name, path, python, requirements, version, c, verbose):
    """Build the package.

    For each template file in bear/templates, read the file in plain text,
    format them with kwarg values and then write them into the new package
    with the approprite suffix.

    Parameters
    ----------
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
        The name of the author

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

    read_write(join(proj_level, ".coveragerc"), write_to_dir=path,
               suffix=None, verbose=verbose, package_name=name)

    read_write(join(proj_level, ".gitignore"), write_to_dir=path,
               suffix=None, verbose=verbose)

    read_write(join(proj_level, ".travis.txt"), write_to_dir=path,
               suffix=".yml", verbose=verbose, package_name=name)

    read_write(join(proj_level, "MANIFEST.txt"), write_to_dir=path,
               suffix=".in", verbose=verbose, package_name=name)

    read_write(join(proj_level, "README.txt"), write_to_dir=path,
               suffix=".md", verbose=verbose, package_name=name,
               bear_version=bear_version, description=description)

    read_write(join(proj_level, "requirements.txt"), write_to_dir=path,
               suffix=".txt", verbose=verbose, requirements=requirements)

    read_write(join(proj_level, "setup.txt"), write_to_dir=path,
               suffix=".py", verbose=verbose, header=header,
               package_name=name, description=description,
               author=author, author_email=email, python_requires=python,
               c=str(c), license=license, git_username=git_user,
               package_name_upper=name.upper())

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


if __name__ == "__main__":
    # This is the argument parser that will parse all the CLI args
    parser = argparse.ArgumentParser(
        description="Bear's mission is to expedite your project's setup time. "
                    "When an idea strikes,the last\nthing that should stand "
                    "between you and your idea is the structural minutiae "
                    "of your project.\nBear assembles a default project "
                    "layout that includes a build script, documentation, and "
                    "examples all ready to be\nfilled in by you, the creative "
                    "genius.",
        formatter_class=RawTextHelpFormatter)

    parser.add_argument("--author", dest="author", type=str,
                        help="The package author's name. This will be included "
                             "in the setup.py. This is optional.")

    parser.add_argument("--c", dest="c", action="store_true",
                        help="Whether Cython code is required for building "
                             "the package. This is optional. Default is False.")

    parser.add_argument("--description", dest="description", type=str,
                        help="The project description. Since this may contain "
                             "spaces, you should surround this in quotes.")

    parser.add_argument("--email", dest="email", type=str,
                        help="The package author's email address. This is "
                             "included in the setup.py. This is optional.")

    parser.add_argument("--git-username", dest="git_user", type=str,
                        help="Your git username. If provided, will include the "
                             "project link in your setup.py.")

    parser.add_argument("--license", dest="license", type=str,
                        help="The package license. This is optional and "
                             "defaults to 'MIT'")

    parser.add_argument("--name", dest="project_name", type=str,
                        help="The name of the package to create. This should "
                             "be a string and should not contain any OS-"
                             "reserved characters.")

    parser.add_argument("--path", dest="path", type=str,
                        help="The absolute path to the directory where the "
                             "package will be created. This is optional. "
                             "Defaults to '.'")

    parser.add_argument("--python", dest="python_requires", type=str,
                        help="A string of the supported python versions. This "
                             "is included in the setup.py. E.g., "
                             "'>=2.7, >=3.5' or '>=3.0'.\nThis is optional and "
                             "will default to '>=3.5'.")

    parser.add_argument("--requirements", dest="requirements", type=str,
                        help="A string consisting of comma-separated "
                             "requirements, which will be written into the "
                             "requirements.txt.")

    parser.add_argument("--verbose", dest="verbose", action="store_true",
                        help="Whether to build in verbose mode, which will "
                             "produce stdout. This is optional and defaults "
                             "to False.")

    parser.add_argument("--version", dest="version", type=str,
                        help="The version of your package. This should be a "
                             "string in the format: <MAJOR>.<MINOR>.<MICRO>, "
                             "i.e., 1.0.5.\nThis is optional. The default "
                             "value is '1.0.0'")

    parser.set_defaults(author="",
                        c=False,
                        description="",
                        email="",
                        git_user="",
                        license="MIT",
                        path=".",
                        project_name=None,
                        python_requires=">=3.5",
                        requirements=None,
                        verbose=False,
                        version="1.0.0")

    # Parse and validate
    parsed_args = parser.parse_args()
    args = validate_args(parsed_args)

    # This is the path where we'll be creating the directory
    pth = args['path']

    # Handle the project level files first
    try:
        make_package(**args)
    except Exception:
        # First, remove the directory
        if os.path.exists(pth):
            shutil.rmtree(pth)

        # Now raise
        raise

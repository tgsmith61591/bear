# -*- coding: utf-8 -*-

from __future__ import absolute_import

from ..utils.io import read_write, copy_to

import os
from os.path import join
import datetime

__all__ = ['make_package']


def _create_project_level(proj_level, path, verbose, name, bear_version,
                          description, requirements, header, author, email,
                          python, c, git_user, license, year):
    """Create the top-level of the project (not the package itself)

    Reads/writes the following files to the top of the project-level, editing
    each template with the package name or other necessary variables::

        .coveragerc
        .gitignore
        .travis.yml
        LICENSE
        MANIFEST.in
        README.md
        requirements.txt
        setup.py
    """
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
               package_name=name, year=year)


def _create_package_level(package_templates, path, c, version, verbose,
                          name, header):
    """Create the package-level files and submodules.

    Reads/writes the following files with the appropriate edits (version, name,
    headers, etc.)::

        {PACKAGE}/__init__.py
        {PACKAGE}/setup.py

    If ``c`` is True, creates the following additional files within the
    {PACKAGE} directory::

        __check_build/
          |__ tests/
          |     |__ __init__.py
          |     |__ test_check_build.py
          |__ __init__.py
          |__ _check_build.pyx
          |__ setup.py

        _build_utils/
          |__ __init__.py

    These utilities are used within the package's ``__init__.py`` to determine
    whether the package was successfully built.

    Parameters
    ----------
    package_templates : str or unicode
        The absolute path to the bear templates directory where the package
        templates are maintained.

    path : str or unicode
        The absolute path to the location where the package will be created.
        The package will be built at ``{path}/name``

    c : bool
        Whether C is required to build the package. If True, two new
        directories will be added to the package::

            __check_build
            _build_utils

    version : str or unicode
        The version of the package to build

    verbose : bool
        Whether to build in verbose mode.

    name : str or unicode
        The name of the package

    header : str or unicode
        The header to place in created templates. Attributes the creation to
        Bear.
    """
    package = join(path, name)
    os.mkdir(package)
    read_write(join(package_templates, "__init__.txt"), write_to_dir=package,
               suffix=".py", verbose=verbose, header=header,
               version=version, package_name_upper=name.upper(),
               package_name=name,

               # If cython build, import the __check_build at the head
               c="from . import __check_build" if c else "")

    # If we are using Cython, then we will not comment out the cythonization
    # lines. Otherwise we will.
    read_write(join(package_templates, "setup.txt"), write_to_dir=package,
               suffix=".py", verbose=verbose, header=header,
               package_name=name,

               # Insert a comment in front of cython lines if not using cython
               comment_for_no_c="# " if not c else "")

    # If we're depending on building C code, we need to create the
    # __check_build and _build_utils submodules
    if c:
        cb_template = join(package_templates, "__check_build")
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
        bu_template = join(package_templates, "_build_utils")
        build_utils = join(package, "_build_utils")
        os.mkdir(build_utils)

        read_write(join(bu_template, "__init__.txt"),
                   write_to_dir=build_utils, suffix=".py",
                   verbose=verbose,
                   package_name=name)


def _create_ci_build_tools(ci_templates, path, name, verbose, c, proj_level,
                           travis, circle):
    """Create the CI build/test scripts.

    Builds CI scripts for Travis and Circle CI. Depending on the versions
    required for the package or the dependencies required (i.e., a non-python
    dependency), these will likely have to be updated by the user
    after-the-fact.

    Parameters
    ----------
    ci_templates : str or unicode
        The build_tools examples directory.

    path : str or unicode
        The absolute path to the location where the package will be created.
        The package will be built at ``{path}/name``

    name : str or unicode
        The name of the package

    verbose : bool
        Whether to build in verbose mode.

    c : bool
        Whether C is required to build the package. If so, the CI build tools
        will be updated accordingly (i.e., GCC requirements, etc.)

    proj_level : str or unicode
        The project-level templates directory.

    circle : bool
        Whether to enable Circle CI tools

    travis : bool
        Whether to enable Travis CI tools
    """
    # Build the build_tools directory
    build_tools = join(path, "build_tools")
    os.mkdir(build_tools)

    # The build_tools templates directories
    circle_level = join(ci_templates, "circle")
    trav_level = join(ci_templates, "travis")

    # Start with Circle CI ----------------------------------------------------
    # Make the .circleci/config.yml first, then move over the build script
    if circle:
        circleci = join(path, ".circleci")
        os.mkdir(circleci)

        copy_to(join(proj_level, ".circleci", "config.yml"),
                write_to_dir=circleci, verbose=verbose)

        # Read/write the build_tools/circle/build_test_pypy.sh
        circle_target = join(build_tools, "circle")
        os.mkdir(circle_target)
        read_write(join(circle_level, "build_test_pypy.txt"),
                   write_to_dir=circle_target,
                   suffix=".sh", verbose=verbose,
                   package_name=name, c="" if not c else " Cython")

    # Now build Travis files --------------------------------------------------
    # Create the build_tools/travis components
    if travis:
        travis_dir = join(build_tools, "travis")
        os.mkdir(travis_dir)

        read_write(join(trav_level, "after_success.txt"),
                   write_to_dir=travis_dir, suffix=".sh", verbose=verbose,
                   package_name=name)

        read_write(join(trav_level, "before_install.txt"),
                   write_to_dir=travis_dir,
                   suffix=".sh", verbose=verbose,
                   c="true" if c else "false")

        read_write(join(trav_level, "before_script.txt"),
                   write_to_dir=travis_dir, suffix=".sh",
                   verbose=verbose)

        copy_to(join(trav_level, "build_manywheels_linux.sh"),
                write_to_dir=travis_dir, verbose=verbose)

        copy_to(join(trav_level, "build_wheels.sh"),
                write_to_dir=travis_dir, verbose=verbose)

        read_write(join(trav_level, "install.txt"), write_to_dir=travis_dir,
                   suffix='.sh', verbose=verbose, c="true" if c else "false")

        copy_to(join(trav_level, "setup.cfg"),
                write_to_dir=travis_dir, verbose=verbose)

        read_write(join(trav_level, "test_script.txt"),
                   write_to_dir=travis_dir, suffix=".sh", verbose=verbose,
                   package_name=name)


def _create_examples_dir(examples_templates, path, verbose, name):
    """Create the examples directory.

    Parameters
    ----------
    examples_templates : str or unicode
        The absolute path to the directory containing the examples templates.

    path : str or unicode
        The absolute path to the location where the package will be created.
        The package will be built at ``{path}/name``

    verbose : bool
        Whether to build in verbose mode.

    name : str or unicode
        The name of the package
    """
    examples = join(path, "examples")
    os.mkdir(examples)
    read_write(join(examples_templates, "README.txt"),
               write_to_dir=examples,
               suffix=".txt", verbose=verbose,
               package_name=name)


def _create_doc(doc_templates, path, name, requirements, verbose,
                bear_version, description, author, year, git_user):
    """Create the documentation for the package.

    This creates a doc/ directory at the project level, and populates the
    Sphinx configuration as well as respective Makefiles.

    Parameters
    ----------
    doc_templates : str or unicode
        The path to the Bear templates for documentation.

    path : str or unicode
        The absolute path to the location where the package will be created.
        The package will be built at ``{path}/name``

    name : str or unicode
        The name of the package

    requirements : str or unicode
        The package requirements to be written in requirements.txt

    verbose : bool
        Whether to build in verbose mode.

    bear_version : str or unicode
        The version of Bear that created the package.

    description : str or unicode
        The description for the package. This is written into the new
        project's setup.py.

    year : str or unicode
        The year for copyright purposes.

    author: str or unicode
        The package author.

    git_user : str or unicode
        The git username of the author.
    """
    # New doc location
    doc_dir = join(path, "doc")
    os.makedirs(doc_dir)

    # Write the make files
    read_write(join(doc_templates, "make.txt"),
               write_to_dir=doc_dir, suffix=".bat",
               verbose=verbose, package_name=name)

    read_write(join(doc_templates, "Makefile"),
               write_to_dir=doc_dir, suffix=None,
               verbose=verbose, package_name=name)

    # Now the RST files
    fmtreq = (lambda req: os.linesep.join(["* " + r for r in req.split(",")]))
    read_write(join(doc_templates, "setup.txt"),
               write_to_dir=doc_dir, suffix=".rst", verbose=verbose,
               package_name=name, bear_version=bear_version,
               requirements=fmtreq(requirements))

    read_write(join(doc_templates, "about.txt"),
               write_to_dir=doc_dir, suffix=".rst", verbose=verbose,
               package_name=name, bear_version=bear_version,
               description=description, hashes="=" * len(name))

    read_write(join(doc_templates, "user_guide.txt"),
               write_to_dir=doc_dir, suffix=".rst", verbose=verbose,
               package_name=name, bear_version=bear_version)

    # Amend the configuration
    linkcode_pattern = ('https://github.com/%(git_user)s/'
                        '%(package_name)s/blob/{revision}/'
                        '{package}/{path}#L{lineno}'
                        % dict(git_user=git_user,
                               package_name=name))
    read_write(join(doc_templates, "conf.txt"),
               write_to_dir=doc_dir, suffix=".py", verbose=verbose,
               package_name=name, bear_version=bear_version,
               author_name=author, year=year, git_user=git_user,
               linkcode_pattern=linkcode_pattern)

    # Sphinxext dir files and other file copies
    sphinxext = join(doc_dir, "sphinxext")
    os.makedirs(sphinxext)
    for f in ("github_link.py", "MANIFEST.in"):
        copy_to(join(doc_templates, "sphinxext", f),
                write_to_dir=sphinxext, verbose=verbose)

    copy_to(join(doc_templates, "README.md"),
            write_to_dir=doc_dir, verbose=verbose)

    # Now for _static, _templates, includes, etc.
    templates = join(doc_templates, "_templates")
    templates_target = join(doc_dir, "_templates")
    os.makedirs(templates_target)
    for f in ("class.rst", "class_with_call.rst", "class_without_init.rst",
              "function.rst", "numpydoc_docstring.rst"):
        copy_to(join(templates, f), write_to_dir=templates_target,
                verbose=verbose)

    static = join(doc_templates, "_static")
    css = join(static, "css")
    css_target = join(doc_dir, "_static", "css")
    os.makedirs(css_target)
    for f in ("style.css",):
        copy_to(join(css, f), write_to_dir=css_target, verbose=verbose)

    includes = join(doc_templates, "includes")
    includes_tgt = join(doc_dir, "includes")
    os.makedirs(includes_tgt)
    copy_to(join(includes, "api_css.rst"), write_to_dir=includes_tgt,
            verbose=verbose)

    # Now for the modules/classes.txt
    modules_templates = join(doc_templates, "modules")
    modules_target = join(doc_dir, "modules")
    os.makedirs(modules_target)

    read_write(join(modules_templates, "classes.txt"),
               write_to_dir=modules_target, suffix=".rst", verbose=verbose,
               bear_version=bear_version, package_name=name)


def make_package(header, bear_location, bear_version,
                 author, description, email, git_user, license,
                 name, path, python, requirements, version, c, verbose,
                 circle, travis):
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

    circle : bool
        Whether to enable Circle CI tools

    travis : bool
        Whether to enable Travis CI tools
    """
    # Make the path for the project
    os.makedirs(path)

    # Project level
    templates = join(bear_location, "templates")
    proj_level = join(templates, "project_level")
    pkg_level = join(templates, "package_level")
    ex_level = join(templates, "examples")
    doc_level = join(proj_level, "doc")
    ci_level = join(templates, "build_tools")

    # in case someone runs this on 12/31 11:59:59, capture this ONCE
    year = str(datetime.datetime.now().year)

    # Create the top level of the project (not the package yet)
    _create_project_level(proj_level=proj_level, path=path, verbose=verbose,
                          name=name, bear_version=bear_version,
                          description=description, requirements=requirements,
                          header=header, author=author, email=email,
                          python=python, c=c, git_user=git_user,
                          license=license, year=year)

    # Now create the package-level
    _create_package_level(package_templates=pkg_level, path=path, c=c,
                          version=version, verbose=verbose, name=name,
                          header=header)

    # Create the CI tools
    _create_ci_build_tools(ci_templates=ci_level, path=path, name=name,
                           verbose=verbose, c=c, proj_level=proj_level,
                           travis=travis, circle=circle)

    # Create the examples directory
    _create_examples_dir(examples_templates=ex_level, path=path,
                         verbose=verbose, name=name)

    # Create the documentation
    _create_doc(doc_templates=doc_level, path=path, name=name,
                requirements=requirements, verbose=verbose,
                bear_version=bear_version, description=description,
                year=year, author=author, git_user=git_user)

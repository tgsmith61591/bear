# -*- coding: utf-8 -*-

from __future__ import absolute_import

import argparse
from argparse import RawTextHelpFormatter

import bear
from bear.defaults import default_values
from bear.utils.validation import validate_args
from bear.utils.yaml import parse_yaml
from bear.core import make_package

import shutil
import sys
import os

# The bear version, used to build the README
bear_version = bear.__version__
bear_location = bear.package_location()

# The header we'll write to the top of all the python files
header = """# -*- coding: utf-8 -*-
# Auto-generated with bear v%s, (c) Taylor G Smith
""" % bear_version


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

    # There are two subparsers we'll use... "create" and "yaml"
    subparsers = parser.add_subparsers(help="Use 'create' to create your "
                                            "package on the CLI, or 'yaml' to "
                                            "create your package from a .yml "
                                            "file configuration")

    # Create the parser for the "create" command, which is probably more likely
    c_parser = subparsers.add_parser("create",
                                     help="Create your package from CLI "
                                          "arguments")
    y_parser = subparsers.add_parser("yaml",
                                     help="Build your package from a .yml "
                                          "configuration. Your YAML file keys "
                                          "should align with the options "
                                          "specifed in the 'bear create' CLI "
                                          "arguments.")

    # "Yaml" args
    y_parser.add_argument("-f", "--file", dest="config_file", type=str,
                          help="The path to the YAML configuration file.")

    # "Create" args
    c_parser.add_argument("--author", dest="author", type=str,
                          help="The package author's name. This will be "
                               "included in the setup.py. This is optional.")

    c_parser.add_argument("--c", dest="c", action="store_true",
                          help="Whether Cython code is required for building "
                               "the package. This is optional. Default is "
                               "False.")

    c_parser.add_argument("--description", dest="description", type=str,
                          help="The project description. Since this may "
                               "contain spaces, you should surround this "
                               "in quotes.")

    c_parser.add_argument("--email", dest="email", type=str,
                          help="The package author's email address. This is "
                               "included in the setup.py. This is optional.")

    c_parser.add_argument("--git_user", dest="git_user", type=str,
                          help="Your git username. If provided, will include "
                               "the project link in your setup.py.")

    c_parser.add_argument("--license", dest="license", type=str,
                          help="The package license. This is optional and "
                               "defaults to 'MIT'. Should be one of 'MIT',"
                               "'BSD-3', or 'GPL'")

    c_parser.add_argument("--project_name", dest="project_name", type=str,
                          help="The name of the package to create. This "
                               "should be a string and should not contain any "
                               "OS-reserved characters.")

    c_parser.add_argument("--path", dest="path", type=str,
                          help="The absolute path to the directory where the "
                               "package will be created. This is optional. "
                               "Defaults to '.'")

    c_parser.add_argument("--python", dest="python", type=str,
                          help="A string of the supported python versions. "
                               "This is included in the setup.py. E.g., "
                               "'>=2.7, >=3.5' or '>=3.0'.\nThis is optional "
                               "and will default to '>=3.5'.")

    c_parser.add_argument("--submodules", dest="submodules", type=str,
                          help="A comma-separated list of submodules to "
                               "create within the new package. Default is "
                               "None.")

    c_parser.add_argument("--requirements", dest="requirements", type=str,
                          help="A string consisting of comma-separated "
                               "requirements, which will be written into the "
                               "requirements.txt.")

    c_parser.add_argument("--verbose", dest="verbose", action="store_true",
                          help="Whether to build in verbose mode, which will "
                               "produce stdout. This is optional and defaults "
                               "to False.")

    c_parser.add_argument("--version", dest="version", type=str,
                          help="The version of your package. This should be a "
                               "string in the format: <MAJOR>.<MINOR>."
                               "<MICRO>, i.e., 1.0.5.\nThis is optional. The "
                               "default value is '1.0.0'")

    # Optional arguments that will enable various CI solutions
    c_parser.add_argument("--circle", dest="circle", action="store_true",
                          help="Whether to create a .circleci/ directory and "
                               "build_tools utilities. If False (by default) "
                               "will not.")

    c_parser.add_argument("--travis", dest="travis", action="store_true",
                          help="Whether to create a .travis.yml and a Travis "
                               "build_tools directory. If False (by default) "
                               "will not.")

    # Default args (store as a dict so we can lookup)
    yaml_defaults = default_values["yaml"]
    create_defaults = default_values["create"]
    y_parser.set_defaults(**yaml_defaults)
    c_parser.set_defaults(**create_defaults)

    # Parse and validate
    parsed_args, unknown_args = parser.parse_known_args()
    # TODO: someday do this better?
    # https://stackoverflow.com/questions/4575747/get-selected-subcommand-with-argparse
    method = sys.argv[1]
    if unknown_args:
        raise ValueError("Unknown arguments for method='{method}': {unknown}"
                         .format(method=method, unknown=str(unknown_args)))

    # If we need to parse the yaml, do so now
    do_parse_yaml = method == "yaml"
    if do_parse_yaml:
        parsed_args = parse_yaml(parsed_args.config_file, create_defaults)

    # Now validate the args and create as normal
    args = validate_args(parsed_args)

    # This is the path where we'll be creating the directory
    pth = args['path']

    # Handle the project level files first
    try:
        make_package(header=header,
                     bear_location=bear_location,
                     bear_version=bear_version,
                     **args)
    except Exception:
        # First, remove the directory
        if os.path.exists(pth):
            shutil.rmtree(pth)

        # Now raise
        raise

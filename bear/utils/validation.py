# -*- coding: utf-8 -*-

from __future__ import absolute_import

import os

__all__ = [
    'validate_path',
    'validate_project_name',
    'validate_requirements'
]


def validate_path(path, name):
    """Validate the location where the path will be written.

    Make sure the path is legal.

    Parameters
    ----------
    path : str, unicode or None
        The absolute path to where the package will be created.

    name : str, unicode or None
        The name of the package to create. Will raise if None or if contains
        illegal characters.

    Returns
    -------
    path : str or unicode
        The path to the package.
    """
    if not path:
        path = "."

    # if the path doesn't end with 'name', make it
    if not path.endswith(name):
        path = os.path.join(path, name)

    # if the path already exists, raise
    if os.path.exists(path):
        raise OSError("Path (%s) already exists!" % path)
    return path


def validate_project_name(name):
    """Validate the project name.

    Make sure the package name is legal and does not contain reserved
    characters. If the name is None, will also raise.

    Parameters
    ----------
    name : str, unicode or None
        The name of the package to create. Will raise if None or if contains
        illegal characters.

    Returns
    -------
    name : str or unicode
        The name of the package.
    """
    if not name:
        raise ValueError("'project_name' is a required argument!")

    # If there are illegal values in the project name, raise
    illegal_intersection = set(name).intersection({
        os.sep, os.linesep, os.pathsep, os.path.sep,
    })

    if illegal_intersection:
        raise ValueError("Illegal value(s) found in project name: %r"
                         % illegal_intersection)

    return name


def validate_requirements(req):
    """Validate the package requirements.

    Validate and format the package requirements to get a new-line separated
    list of requirements to write to requirements.txt. Also, since Numpy is
    required to build the package that's generated, if Numpy is not present
    in the requirements, it will be added.

    Parameters
    ----------
    req : str, unicode or None
        The requirements. Should be a comma-separated list of requirements
        that will be written to 'requirements.txt' split across new lines.

    Returns
    -------
    new_requirements : str or unicode
        A string of requirements separated by newline characters to be
        written into requirements.txt
    """
    req = "" if not req else req
    requirements = [
        token.strip()
        for token in req.replace(os.linesep, ",").split(",")
    ]

    # Validate that numpy is present, and if not we'll use 1.12 as a floor
    numpy_found = False
    new_requirements = []  # filter out non truthy ones in this pass also
    for req in requirements:
        if req.lower().startswith("numpy"):
            numpy_found = True
        # Filter out the non-truthy ones
        if not req:
            continue
        else:
            new_requirements.append(req)
    # if it's not there, add it
    if not numpy_found:
        new_requirements.append("numpy>=1.12")
    return os.linesep.join(new_requirements)

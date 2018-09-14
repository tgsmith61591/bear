# -*- coding: utf-8 -*-

from __future__ import absolute_import

import six
import os

__all__ = [
    'validate_args',
    'validate_path',
    'validate_project_name',
    'validate_requirements'
]


def validate_args(args):
    """Get the validated args.

    The project name is validated to be non-null and not contain illegal
    characters, the requirements are validated, and the path is validated
    to end with the ``name`` parameter.

    Returns
    -------
    vargs : dict
        A dictionary of validated arguments.
    """
    # The project name is the only real required value
    nm = validate_project_name(args.project_name)

    # Validate requirements, if any...
    req = validate_requirements(args.requirements, args.c)

    # Validate path
    path = validate_path(args.path, nm)

    # Validate the license
    license = validate_license(args.license)

    return dict(author=args.author,
                c=args.c,
                description=args.description,
                email=args.email,
                git_user=args.git_user,
                license=license,
                name=nm,
                path=path,
                python=args.python_requires,
                requirements=req,
                verbose=args.verbose,
                version=args.version)


def validate_license(license):
    """Validate the license.

    Make sure the provided license is one that exists within the
    Bear templates.

    Parameters
    ----------
    license : str or unicode
        The name of the license to assign the package. Will raise if the
        license does not exist.

    Returns
    -------
    license : str or unicode
        The name of the license.
    """
    # These are the names of the existing licenses
    valid = {'BSD-3', 'GPL', 'MIT'}
    license_u = license.upper()

    if license_u not in valid:
        raise ValueError("Expected license to be in %s, but got %s"
                         % (str(valid), license))

    return license_u


def validate_path(path, name):
    """Validate the location where the path will be written.

    Make sure the path is legal. If the path is not truthy, set it to "."
    (here). Next, if the path does not end with the ``name``, set the path
    to end with ``name``.

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

    # if the path doesn't end with 'name', make it. We have also already
    # validated that the name is not '.' or '..' so we don't get './.' or
    # anything dangerous
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

    # If the name is '.' or any variant therein... we need to raise
    sname = set(name)
    if sname == {'.'}:
        raise ValueError("Cannot set 'project_name' to %s" % name)

    # If there are illegal values in the project name, raise
    illegal_intersection = sname.intersection({
        os.sep, os.linesep, os.pathsep, os.path.sep,
    })

    if illegal_intersection:
        raise ValueError("Illegal value(s) found in project name: %r"
                         % illegal_intersection)

    return name


def validate_requirements(req, cython_required):
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

    cython_required : bool
        Whether cython is required to build the project. If so, it will be
        validated that cython exists in the requirements.

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

    # Hard requirements. Numpy is ALWAYS required, but cython is only if
    # cython_required
    hard_requirements = dict(numpy=">=1.12")
    if cython_required:
        hard_requirements['cython'] = '>=0.23'

    # For each requirement, determine whether it's in the hard requirements
    new_requirements = []
    for req in requirements:
        # Re-assign the hard-requirements ref to remove the ones that are
        # already present
        hard_requirements = {pkg: ver
                             for pkg, ver in six.iteritems(hard_requirements)
                             if not req.lower().startswith(pkg)}
        # Filter out the non-truthy ones
        if not req:
            continue
        else:
            new_requirements.append(req)
    # if there are still requirements, append them
    for k, v in six.iteritems(hard_requirements):
        new_requirements.append(k + v)
    return os.linesep.join(new_requirements)

# -*- coding: utf-8 -*-

from __future__ import absolute_import

from shutil import copyfile
from os.path import join
import os

__all__ = [
    'copy_to',
    'read_write'
]


def copy_to(copy_from_file, write_to_dir, verbose=False):
    """Copy a template file elsewhere.

    This executes a ``cp`` on a file into a new directory leaving the
    original file intact.

    Parameters
    ----------
    copy_from_file : str or unicode
        The absolute path to the file that will be copied from the bear
        templates directory.

    write_to_dir : str or unicode
        The absolute path to the file that will be written in the new
        python package.

    verbose : bool, optional (default=False)
        Whether to print what's being written.
    """
    # Get the filename
    file_name = copy_from_file.split(os.sep)[-1]
    out_file_name = join(write_to_dir, file_name)

    # Print it if needed
    if verbose:
        print("Formatting %s template into %s"
              % (copy_from_file, out_file_name))

    copyfile(copy_from_file, out_file_name)


def read_write(read_from_file, write_to_dir, suffix=None, verbose=False,
               overwrite_name=None, **kwargs):
    """Read a template and write it as a package file.

    Loads a bear template file, formats it with the provided args and then
    will write it to a package file with a provided suffix.

    Parameters
    ----------
    read_from_file : str or unicode
        The absolute path to the file that will be read from the bear
        templates directory.

    write_to_dir : str or unicode
        The absolute path to the file that will be written in the new
        python package.

    suffix : str, unicode or None, optional (default=None)
        The file extension for the new file that will be written.

    verbose : bool, optional (default=False)
        Whether to print what's being written.

    overwrite_name : str, unicode or None, optional (default=None)
        If you'd like to overwrite the name of the file, this is the parameter
        you'd use. Note that this will override the ``suffix`` command.

    **kwargs : keyword args or dict
        The arguments used to format the file that's read in.
    """
    # Read a file and write it to a location
    with open(read_from_file, "r") as read_in:
        content = read_in.read().format(**kwargs)

    if not overwrite_name:
        # Get the prefix of the file
        file_name = read_from_file.split(os.sep)[-1]

        # If the suffix is None, get a blank string. Otherwise ensure it
        # starts with a "."
        suffix = "" if suffix is None \
            else suffix if suffix.startswith(".") \
            else "." + suffix

        # Get the name of the file without an extension (if one is present)
        last_dot_idx = file_name.rfind(".")
        if last_dot_idx > 0:
            # e.g., something.txt
            file_no_extension = file_name[:last_dot_idx] + suffix
        else:
            # e.g., .coveragerc
            file_no_extension = file_name

        out_file_name = join(write_to_dir, file_no_extension)

    # If we're overwriting, we'll just take the name that's given
    else:
        out_file_name = join(write_to_dir, overwrite_name)

    # Print it if needed
    if verbose:
        print("Formatting %s template into %s"
              % (read_from_file, out_file_name))

    with open(out_file_name, "w") as out:
        out.write(content)

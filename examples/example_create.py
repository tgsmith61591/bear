"""
=====================
Simple package create
=====================


It's unlikely you'd create a new package from within a Python script, but here
is an example of how you can leverage the package internals for exactly that
purpose.

.. raw:: html

   <br/>
"""
print(__doc__)

# Author: Taylor Smith <taylor.smith@alkaline-ml.com>

from bear.core import create
import bear
import datetime
from os.path import join
import os

# Attrs of the bear package
bear_location = bear.package_location()
bear_version = bear.__version__
year = str(datetime.datetime.now().year)

# Attrs of the TEST package we want to create
project_path = "bear_test_project_dir"
package_name = "bear_test"
path = join(project_path, package_name)
author = "Fake Authorman"
email = "some_email@fake.com"
python = "3.5"
git_user = "fakegituser"
lic = "MIT"
description = "This is a test pkg"

# Call the make package (but only on Circle)
if os.environ.get("BUILD_EXAMPLES", "false") == "true":
    create.make_package(header="File header", bear_location=bear_location,
                        bear_version=bear_version, author=author,
                        description=description, email=email,
                        git_user=git_user, license=lic, name=package_name,
                        path=path, python=python, requirements="numpy",
                        version="1.0.0", c=False, verbose=True, circle=True,
                        travis=True, submodules="utils")

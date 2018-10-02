.. _api_ref:

=============
API Reference
=============

.. include:: ../includes/api_css.rst

This is the class and function reference for Bear. Please refer to
the :ref:`full user guide <user_guide>` for further details, as the class and
function raw specifications may not be enough to give full guidelines on their
uses.


.. _core_ref:

:mod:`bear.core`: Core Bear functionality
=========================================

The ``bear.core`` sub-module defines the core functionality and templating
behavior of the package.

.. automodule:: bear.core
    :no-members:
    :no-inherited-members:

Core package creation
---------------------

There's only one public method in the core submodule.

.. currentmodule:: bear

.. autosummary::
    :toctree: generated/
    :template: function.rst

    core.make_package


.. _utils_ref:

:mod:`bear.utils`: Utilities
============================

Utilities, IO and validation functions used across the package.

.. automodule:: bear.utils
    :no-members:
    :no-inherited-members:

IO utilities
------------

Utilities for reading/copying templates and formatting them.

.. currentmodule:: bear

.. autosummary::
    :toctree: generated/
    :template: function.rst

    utils.copy_to
    utils.read_write

Validation functions
--------------------

.. currentmodule:: bear

.. autosummary::
    :toctree: generated/
    :template: function.rst

    utils.validate_args
    utils.validate_license
    utils.validate_path
    utils.validate_project_name
    utils.validate_requirements

YAML-parsing functions
----------------------

.. currentmodule:: bear

.. autosummary::
    :toctree: generated/
    :template: function.rst

    utils.parse_yaml

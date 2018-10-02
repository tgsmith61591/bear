.. _setup:

=====
Setup
=====

Bear depends on a couple prominent python packages:

* `Numpy <https://github.com/numpy/numpy>`_
* `PyYaml <https://pyyaml.org>`_

Build from source
-----------------

As of v0.1.9, Bear is not yet on PyPi. You'll need to first clone it from Git:

.. code-block:: bash

    $ git clone https://github.com/tgsmith61591/bear.git
    $ cd bear

To build in development mode (for running unit tests):

.. code-block:: bash

    $ python setup.py develop

Alternatively, to install the package in your ``site-packages``:

.. code-block:: bash

    $ python setup.py install

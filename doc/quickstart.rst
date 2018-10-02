.. _quickstart:

===============
Bear Quickstart
===============

As of v0.1.9, there are two modes for using Bear. ``create`` mode allows a user
to specify project requirements on the commandline. ``yaml`` mode allows a user
to build a package from a YAML configuration file.

Command line interface
----------------------

Building a package from the command line with Bear is simple. To run from the CLI,
use the ``bear create`` directive:

.. code-block:: bash

    $ python -m bear create ...

There are numerous options available (all viewable with ``python -m bear create --help``).
Here are a few examples of package configurations you could use:

A simple Python package with no Cython
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    $ python -m bear create --project_name simple_project

A Python package with Cython (created in verbose mode)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    $ python -m bear create \
        --project_name cython_project \
        --verbose \
        --c

A package with CI configs for Travis and Circle CI
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    $ python -m bear create \
        --project_name cicd_project \
        --travis \
        --circle

.. _kafkaesque:

A meticulously-designed package
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    $ python -m bear create \
        --project_name detailed_package \
        --author "Franz Kafka" \
        --description "A very detailed project" \
        --email "franz.kafka@kafkaesque.net" \
        --git_user "franzkafka1883" \
        --license MIT \
        --python ">=3.5" \
        --path . \
        --submodules "utils,misc" \
        --requirements "scikit-learn,scipy,pandas" \
        --version "1.1.5" \
        --verbose \
        --c \
        --travis \
        --circle


From YAML configuration
-----------------------

Anything you can build from the command line, you can build from a YAML config
file (perhaps even more easily). Imagine we wanted to create the exact same
"kafka-esque" example as above (as shown in :ref:`kafkaesque`).

Given the following YAML file:

.. code-block:: yaml

    # config.yml
    project_name: "detailed_package"
    author: "Franz Kafka"
    description: "A very detailed project"
    email: franz.kafka@kafkaesque.net
    git_user: "franzkafka1883"
    license: MIT
    python: ">=3.5"
    submodules: "utils,misc"
    requirements: "scikit-learn, scipy, pandas"
    version: "1.1.5"
    verbose: true
    c: true
    travis: true
    circle: true


We can create the same exact package with the ``bear yaml`` directive:

.. code-block:: bash

    $ python -m bear yaml --file config.yml

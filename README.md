# :grapes: bear

[![Linux build status](https://travis-ci.org/tgsmith61591/bear.svg?branch=master)](https://travis-ci.org/tgsmith61591/bear)
[![PyPy build](https://circleci.com/gh/tgsmith61591/bear.svg?style=svg)](https://circleci.com/gh/tgsmith61591/bear)
[![codecov](https://codecov.io/gh/tgsmith61591/bear/branch/master/graph/badge.svg)](https://codecov.io/gh/tgsmith61591/bear)
![Supported versions](https://img.shields.io/badge/python-2.7,3.5+-blue.svg)


*Create more. Innovate more easily. Bear fruit more quickly.*

Bear helps to structurally automate creating a python package and
its corresponding documentation and CI/CD pipelines so a developer
can jump right into developing the next big thing.


### What is it?

Often times a developer is struck with an idea and then ends up spending valuable
time that could be spent prototyping just putting together the structure of a
project (including doc, CI/CD pipelines, etc.). Bear streamlines that to allow
you to move straight into the code-writing.

After bear is installed, you can start creating new project skeletons right away.
There are two options for creating projects with bear:

* "create"
* "yaml"


#### "Create"

The fastest way to use bear is from the CLI with `create` mode:

```bash
$ python -m bear create --project_name my_project
```

With the `create` command, you can get as complicated as you like:

```bash
$ python -m bear create \
  --path . \
  --project_name new_project \
  --git_user newBearUser42 \
  --python ">=3.5" \
  --requirements "numpy,scipy,scikit-learn" \
  --version 1.0.0 \
  --verbose
```

#### "Yaml"

You can do the same thing with a YAML file. To create the exact same package
as above with a YAML file:

```yaml
# config.yml
path: .
project_name: new_project
git_user: newBearUser42
python: ">=3.5"
requirements: numpy,scipy,scikit-learn
version: "1.0.0"
verbose: true
```

...and running the package:

```bash
$ python -m bear yaml --file config.yml
```

**Note that any option on the command line is available via YAML and goes by the same key.**

## Including CI tools

You can make your life easier by adding auto-configured CI tools and 
configuration files to your package. As of v1.0.9, the following CI/CD tools are
available and can be added with the respective options:

* Travis CI (`--travis`)
    
    Auto-includes `build_tools/travis` helper scripts for testing and deploying on Linux
    and Mac OS, as well as a `.travis.yml` file.
    
* Circle CI (`--circle`)

    Auto-includes a `.circleci/config.yml` file as well as a test runner in `build_tools/circle/build_test_pypy.sh`
    for testing PyPy distributions of Python.
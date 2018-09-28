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
  --version 1.0.0
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
```

...and running the package:

```bash
$ python -m bear yaml --file config.yml
```

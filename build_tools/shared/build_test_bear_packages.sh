#!/bin/bash
# Tests creating packages using Bear both on CLI and YAML. This is
# intended to be called from within a conda or virtual env, and depends
# on the following environment variables:
#
#   PYTHON_VERSION
#   SKIP_TESTS

set -e


virtualenv_install() {
    pip install -vv -e .
}

conda_install() {
    python setup.py install
}

# For installing the package on either a Conda dist or Virtual env dist
install_package() {
    if [[ "$TESTING_ON_CIRCLE" == "true" ]]; then
        virtualenv_install
    else
        conda_install
    fi
}

# Test using bear to create a new package
test_create_new_package_cli() {
    test_package_location="bear_cli_test_package"
    test_package_name="cli_test_package"

    mkdir -p ${test_package_location}
    cd ${test_package_location}

    # Test creating a packing from CLI
    python -m bear create \
      --project_name "${test_package_name}" \
      --python ">={PYTHON_VERSION}" \
      --git_user "tgsmith61591" \
      --version "1.1.1" \
      --verbose

    # CD in, setup the package and test that we can load stuff
    echo "Setting up test python pkg"
    cd ${test_package_name}
    install_package

    # The version should be 1.1.1
    echo "Importing test python pkg"
    test_pkg_vsn=`python -c "import ${test_package_name} as p; print(p.__version__)"`
    cd ..

    # Assert
    if [[ ${test_pkg_vsn} == "1.1.1" ]]; then
        echo "Passed!"
    else
        echo "Expected '1.1.1' but got ${test_pkg_vsn}"
        exit 19
    fi
}

test_create_new_package_yaml() {
    yaml_proj_path="test_yaml_project"
    yaml_pkg_name="test_yaml_package"

    mkdir -p ${yaml_proj_path}
    cd ${yaml_proj_path}

    # Test creating from YAML
    echo "project_name: ${yaml_pkg_name}" > config.yml
    echo "python: '>=${PYTHON_VERSION}'" >> config.yml
    echo "git_user: tgsmith61591" >> config.yml
    echo "version: '1.1.5'" >> config.yml
    echo "verbose: true" >> config.yml

    # This tests that we can install requirements via setup
    echo "requirements: numpy,scikit-learn" >> config.yml

    # Let's also test with CI tools in here
    echo "travis: true" >> config.yml
    echo "circle: true" >> config.yml

    # Actually set it up with bear
    python -m bear yaml --file config.yml

    # CD in, setup the package and test that we can load stuff
    echo "Setting up YAML test python pkg"
    cd ${yaml_pkg_name}
    install_package

    # The version should be 1.1.5
    echo "Importing test YAML python pkg"
    test_yaml_pkg_vsn=`python -c "import ${yaml_pkg_name} as p; print(p.__version__)"`
    cd ..

    # Assert
    if [[ ${test_yaml_pkg_vsn} == "1.1.5" ]]; then
        echo "Passed!"
    else
        echo "Expected '1.1.5' but got ${test_yaml_pkg_vsn}"
        exit 22
    fi
}

if [[ "$SKIP_TESTS" != "true" ]]; then

    # If we're on Circle make sure we have the virtualenv activated
    if [[ "$TESTING_ON_CIRCLE" == "true" ]]; then
        source pypy-env/bin/activate || echo "Virtualenv is already activated"
    fi

    test_create_new_package_cli
    test_create_new_package_yaml
fi

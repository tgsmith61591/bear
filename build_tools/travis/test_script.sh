#!/bin/bash
# This script is meant to be called by the "script" step defined in
# .travis.yml. See http://docs.travis-ci.com/ for more details.
# The behavior of the script is controlled by environment variables defined
# in the .travis.yml in the top level folder of the project.

# License: 3-clause BSD

set -e

python --version
python -c "import numpy; print('numpy %s' % numpy.__version__)"
python -c "\
try:
    import pandas
    print('pandas %s' % pandas.__version__)
except ImportError:
    pass
"
python -c "import multiprocessing as mp; print('%d CPUs' % mp.cpu_count())"

run_tests() {
    TEST_CMD="pytest --showlocals --durations=20 --pyargs"

    # Get into a temp directory to run test from the installed package and
    # check if we do not leave artifacts
    mkdir -p $TEST_DIR

    # We need the setup.cfg & .coveragerc for the test settings
    # (setup.cfg can only be used in Travis since we CANNOT doctest in
    # Appveyor without it complaining about whitespace unnecessarily)
    cp build_tools/travis/setup.cfg $TEST_DIR
    cp .coveragerc $TEST_DIR
    cd $TEST_DIR

    if [[ "$COVERAGE" == "true" ]]; then
        TEST_CMD="$TEST_CMD --cov-config .coveragerc --cov bear"
    fi
    $TEST_CMD bear

    # go back again
    cd $OLDPWD
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
    cd ${test_package_name} && python setup.py install

    # The version should be 1.1.1
    echo "Importing test python pkg"
    test_pkg_vsn=`python -c "import ${test_package_name} as p; print(p.__version__)"`
    cd $OLDPWD

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
    cd ${yaml_pkg_name} && python setup.py install

    # The version should be 1.1.5
    echo "Importing test YAML python pkg"
    test_yaml_pkg_vsn=`python -c "import ${yaml_pkg_name} as p; print(p.__version__)"`
    cd $OLDPWD

    # Assert
    if [[ ${test_yaml_pkg_vsn} == "1.1.5" ]]; then
        echo "Passed!"
    else
        echo "Expected '1.1.5' but got ${test_yaml_pkg_vsn}"
        exit 22
    fi
}

if [[ "$SKIP_TESTS" != "true" ]]; then
    run_tests
    test_create_new_package_cli
    test_create_new_package_yaml
fi

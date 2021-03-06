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

if [[ "$SKIP_TESTS" != "true" ]]; then
    run_tests
fi

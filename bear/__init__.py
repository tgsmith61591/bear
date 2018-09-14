# -*- coding: utf-8 -*-

__version__ = '0.1.5'

try:
    # This variable is injected in the __builtins__ by the build
    # process. It is used to enable importing subpackages of bear when
    # the binaries are not built
    __BEAR_SETUP__
except NameError:
    __BEAR_SETUP__ = False

if __BEAR_SETUP__:
    import sys as _sys
    _sys.stdout.write('Partial import of bear during the build process.\n')
    del _sys
else:
    __all__ = [
        # submodules
        'core',
        'templates',
        'utils'
    ]


# function for finding the package
def package_location():
    import os
    return os.path.abspath(os.path.dirname(__file__))


def setup_module(module):
    # Fixture to assure global seeding of RNG
    import numpy as np
    import random

    _random_seed = int(np.random.uniform() * (2 ** 31 - 1))
    np.random.seed(_random_seed)
    random.seed(_random_seed)

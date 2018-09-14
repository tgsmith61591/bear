# -*- coding: utf-8 -*-
#
# Author: Taylor Smith <taylor.smith@alkaline-ml.com>

from __future__ import print_function, division, absolute_import

import os


# DEFINE CONFIG
def configuration(parent_package='', top_path=None):
    from numpy.distutils.misc_util import Configuration

    libs = []
    if os.name == 'posix':
        libs.append('m')

    config = Configuration('bear', parent_package, top_path)

    # modules
    config.add_subpackage('core')
    config.add_subpackage('templates')
    config.add_subpackage('utils')

    # module tests -- must be added after others!
    config.add_subpackage('core/tests')
    config.add_subpackage('templates/tests')
    config.add_subpackage('utils/tests')
    return config


if __name__ == '__main__':
    from numpy.distutils.core import setup
    setup(**configuration(top_path='').todict())

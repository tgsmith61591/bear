# -*- coding: utf-8 -*-
#
# Dictionaries mapping default values for parsers

from __future__ import absolute_import

# A dictionary mapping each method to its default key/values
default_values = dict(yaml=dict(config_file=None),
                      create=dict(author="",
                                  c=False,
                                  description="",
                                  email="",
                                  git_user="",
                                  license="MIT",
                                  path=".",
                                  project_name=None,
                                  python=">=3.5",
                                  requirements=None,
                                  verbose=False,
                                  version="1.0.0",

                                  # CI solutions
                                  circle=False,
                                  travis=False
                                  )
                      )

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re

from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'ffs/__init__.py')) as f:
    version = re.search("^__version__ = '(\d\.\d+\.\d+(\.?(dev|a|b|rc)\d?)?)'$",
                  f.read(), re.M).group(1)
setup(name='ffs',
      version=version,
      description='simple fuzzy functional system (ffs)',
      url='',
      author='Lukasz Szydlowski',
      author_email='',
      license='GNU GPL v.3',
      packages=['ffs'],
      zip_safe=False)
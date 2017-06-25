#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Setup for flask-monitor
"""

import os
from setuptools import setup, find_packages

__version_info__ = (0, 2, 3)
__version__ = '.'.join([str(val) for val in __version_info__])

__namepkg__ = "flask-monitor"
__desc__ = "Flask Monitor module"
__urlpkg__ = "https://github.com/fraoustin/flask-monitor.git"
__entry_points__ = {}

HERE = os.path.abspath(os.path.dirname(__file__))

# README AND CHANGES
with open(os.path.join(HERE, 'README.rst')) as readme:
    with open(os.path.join(HERE, 'CHANGES.rst')) as changelog:
        LONG_DESC = readme.read() + '\n\n' + changelog.read()
# REQUIREMENTS
with open('REQUIREMENTS.txt') as f:
    REQUIRED = f.read().splitlines()
# CLASSIFIERS
with open('CLASSIFIERS.txt') as f:
    CLASSIFIED = f.read().splitlines()
# AUTHORS
with open('AUTHORS.txt') as f:
    DATA = f.read().splitlines()
    AUTHORS = ','.join([i.split('::')[0] for i in DATA])
    AUTHORS_EMAIL = ','.join([i.split('::')[1] for i in DATA])

setup(
    name=__namepkg__,
    version=__version__,
    packages=find_packages(),
    author=AUTHORS,
    author_email=AUTHORS_EMAIL,
    description=__desc__,
    long_description=LONG_DESC,
    include_package_data=True,
    install_requires=REQUIRED,
    url=__urlpkg__,
    classifiers=CLASSIFIED,
    entry_points=__entry_points__
)

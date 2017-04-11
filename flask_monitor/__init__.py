#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Module flask_monitor
"""

__version_info__ = (0, 1, 0)
__version__ = '.'.join([str(val) for val in __version_info__])

from .main import *
from .log import ObserverLog as ObserverLog 

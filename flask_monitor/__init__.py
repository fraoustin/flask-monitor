#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Module flask_monitor
"""

__version_info__ = (0, 2, 0)
__version__ = '.'.join([str(val) for val in __version_info__])

__namepkg__ = "flask-monitor"
__desc__ = "Flask Monitor module"
__urlpkg__ = "https://github.com/fraoustin/flask-monitor.git"
__entry_points__ = {}

from flask_monitor.main import *
from flask_monitor.log import ObserverLog as ObserverLog 

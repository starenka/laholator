#!/usr/bin/env python
# -*- coding: utf-8 -*-

from settings.base import *
from settings.production import *

try:
    from settings.local import *
except ImportError:
    pass
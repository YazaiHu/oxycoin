# -*- encoding: utf8 -*-
# © Toons

from .. import __FROZEN__
import os, sys

ROOT = os.path.normpath(os.path.abspath(os.path.dirname(sys.executable) if __FROZEN__ else __path__[0]))

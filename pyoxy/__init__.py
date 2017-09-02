# -*- encoding: utf8 -*-
# © Toons

import os, imp, sys, logging

logging.getLogger('requests').setLevel(logging.CRITICAL)
__PY3__ = True if sys.version_info[0] >= 3 else False
__FROZEN__ = hasattr(sys, "frozen") or hasattr(sys, "importers") or imp.is_frozen("__main__")

# deal with home and root directory
HOME = os.path.normpath(os.path.abspath(os.path.dirname(sys.executable if __FROZEN__ else __file__)))
if sys.platform.startswith("win"):
	ROOT = HOME
elif "HOME" in os.environ:
	ROOT = os.environ["HOME"]
else:
	ROOT = os.path.join(os.enfiron["HOMEDRIVE"], os.environ["HOMEPATH"])

# setup a log file
logging.basicConfig(
	filename  = os.path.normpath(os.path.join(ROOT, __name__+".log")) if __FROZEN__ else os.path.normpath(os.path.join(HOME, "."+__name__)),
	format    = '[...][%(asctime)s] %(message)s',
	level     = logging.INFO,
)

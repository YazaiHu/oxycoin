# -*- coding:utf-8 -*-
# created by Toons on 01/05/2017

import os, sys
sys.path.append(os.path.join(os.path.dirname(sys.executable), "site-packages.zip"))

from pyoxy import cli
from pyoxy import api

if __name__ == "__main__":
	api.use("oxy")
	from pyoxy.ui import widgets
	widgets.AddressPanel(padding=4).pack(fill="both")
	widgets.yawTtk.Separator(padding=4).pack(fill="x")

	widgets.SharePannel(padding=4).pack(fill="both")

	secret = widgets.SecretFrame(padding=4, border=3).pack(fill="both")
	widgets.yawTtk.Button(text="Share", state="active", command=lambda w=secret:[print(secret.getKeys())]).pack(anchor="e", padx=8, pady=8).mainloop()

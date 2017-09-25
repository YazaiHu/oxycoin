# -*- coding:utf-8 -*-
# created by Toons on 01/05/2017

import os, sys
sys.path.append(os.path.join(os.path.dirname(sys.executable), "site-packages.zip"))

from pyoxy import api, util, cfg
from pyoxy.ui import widgets

if __name__ == "__main__":

	_exit=\
	"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAAZiS0dEAP8A/wD/oL2nkwAAAAlwSFlzAAAG7AAABuwBHnU4NQAAAAd0SU1FB9sMFws0LDm0tJ4AAAKWSURBVDjLjZJNSxtR"\
	"FIafO6OGMaMkuhCF0A8DAbd1W8yq1IWbQin40eImLjSiXUhIgwS1aiOoiY2g4sIPuutKqq104V9QpCK0pV0NipQx6kykzp0ubIJSW3p2997zPuflvQduqImJCQBGRka6BwYGRgESiQT/VWNjYwBMT0/3ZDIZN5vN"\
	"ut3d3c8BOjs7/+gXN0FSqVSitrZ22DRN6TgOiqIo29vb0cXFxdd/ndzX14frusVzf39/aHZ21k2n0y7gK9xvbGyg63qxrwSgtbWVqakphBBks9m3uVzuVmVlZZuqqti2DeCmUqmvpmm+aW5uTmxtbREOhwFQAObn"\
	"5xFCsLCw8KW6uvqREOJHPp/H4/HgOA6AUFU1FwgEXsTj8dVwOMzMzMwloKOjA13XmZubG9N1/a6UEsMw3juO49E0DSklQOn5+fmOlJL6+vq2SCTSEo1GLwErKysAlJeXxwD29vZW0un0pGmaOcMwPliWtSmEkPF4"\
	"/Klt258dxyEUCqWvZTA5OXm/pKSEi4sLhoeHewFGR0e/AQ+vBn16ehqtqKjY8Pv9dwAVcJTfbwGAk5MTAPNvP7W7u7vtui6KolBTUxMohuj1eg9d10XTtH8uWTAYrAWQUnJwcHBYBHR1dX0sAHp6enoB2tvbi8Kh"\
	"oSEAfD5fDOD4+PgUsACUQppnZ2frUkoaGxvTTU1N91ZXV4uAwcFBYrFYRNO0x0IIDMN4eeMqLy0tuaWlpQWLm7Ztr5eVlXm8Xu8zv9/fcHR0hGVZ32Ox2O2CRrlqcXl52W9ZlqWqKnV1dQ+CweB0IBB4VVVV1aAo"\
	"Cvl8fqcgDoVC1x0kk0mSySQA4+PjEZ/P9wSoB346jvNpf39/PpPJvANoaWlhbW0NgF/89hAL3mpSPAAAAABJRU5ErkJggg=="\

	api.use("toxy")

	# main window
	root = widgets.yawTtk.Tkinter.Tk()
	if not api.__PY3__:
		root.tk.eval("package require Img")
	root.withdraw()

	# tweak data view layout
	style = widgets.yawTtk.Style()
	style.layout("Treeview", "Treeview.treearea -sticky nswe")

	toplevel = widgets.yawTtk.Toplevel(root)
	toplevel.withdraw()
	toplevel["border"] = 0

	address = widgets.AddressPanel(toplevel, padding=4).pack(fill="x")
	widgets.yawTtk.Separator(toplevel).pack(fill="x")

	amount = widgets.ShareFrame(toplevel, padding=4).pack(fill="x")
	widgets.yawTtk.Separator(toplevel).pack(fill="x")

	options = widgets.OptionPannel(toplevel, padding=4).pack(fill="both")
	widgets.yawTtk.Separator(toplevel).pack(fill="x")

	payout = widgets.PayoutFrame(toplevel, padding=4, height=0).pack(fill="both", expand=True)
	widgets.yawTtk.Separator(toplevel).pack(fill="x")

	secret = widgets.SecretFrame(toplevel, padding=4, border=3).pack(anchor="s", fill="x")

	button = widgets.yawTtk.Button(toplevel, text="Share", default="active").pack(side="bottom", anchor="se", padx=8, pady=8)

	def clearPayroll():
		button["command"] = launchPayroll
		payout.data.rows = []
		payout.data.populate()
		button["text"] = "Share"

	def launchPayroll():
		button["command"] = clearPayroll
		button.state("!disabled")
		payout.broadcast()
		button.state("disabled")
		button["text"] = "Clear"

	button.state("disabled")
	button["command"] = launchPayroll
	button["background"] = toplevel["background"]

	MEMORY = {}

	def checkIfAddressChanged():
		global MEMORY
		known = MEMORY.get("address", "")
		actual = address.wallet.get().strip()
		if actual != known:
			MEMORY["address"] = actual
			return True
		else:
			return False

	def checkIfShareChanged():
		global MEMORY
		known = MEMORY.get("share", 0)
		actual = widgets.ShareFrame.satoshi
		if actual != known:
			MEMORY["share"] = actual
			return True
		else:
			return False

	def checkIfNeedAnalyse():
		global MEMORY
		result = False
		for key in ["delay"]:
			known = MEMORY.get(key, None)
			actual = widgets.OptionPannel.options.get(key, None)
			if actual != known:
				MEMORY[key] = actual
				result = True
			else:
				result = False
			if result:
				return result

	def checkIfNeedUpdate():
		global MEMORY
		result = False
		for key in ["lowest", "blacklist", "highest"]:
			known = MEMORY.get(key, None)
			actual = widgets.OptionPannel.options.get(key, None)
			if actual != known:
				MEMORY[key] = actual
				result = True
			else:
				result = False
			if result:
				return result

	def memorize():
		MEMORY.update(**widgets.OptionPannel.options)
		MEMORY.update(address=address.wallet.get().strip())

	def disable():
		address.combo.state("disabled")
		options.disable()

	def enable():
		address.combo.state("!disabled")
		options.enable()

	@util.setInterval(1)
	def heartBeat():
		if not payout.busy:
			if checkIfAddressChanged():
				disable()
				options.saveConf()
				address.update()
				options.loadConf()
				memorize()
				payout.analyse()
				payout.update()
				enable()
			if checkIfNeedAnalyse():
				disable()
				options.saveConf()
				payout.analyse()
				payout.update()
				enable()
			if checkIfShareChanged() or checkIfNeedUpdate():
				options.saveConf()
				payout.update()

		secret.update()
		if secret.check() and widgets.ShareFrame.satoshi > 10000000:
			toplevel["background"] = "lightgreen"
			button.state("!disabled")
		else:
			toplevel["background"] = "red"
			button.state("disabled")

	def useNetwork(network):
		try:
			api.use(network)
		except:
			pass
		else:
			toplevel.tk.setvar("ui.network", network)
			address.wallet.set("")
			combovalues = amount.combo["values"]
			amount.combo.configure(values=(cfg.symbol, ) + combovalues[1:])
			if amount.what.get() not in amount.combo["values"]:
				amount.what.set(cfg.symbol)
			else:
				amount.what.set(amount.what.get())
			toplevel.title("Pool Payout - %s network"%network.capitalize())

	def exit():
		options.saveConf()
		__heartbeat.set()
		sys.exit()

	# menu widget
	menubar = widgets.yawTtk.Menu(root)
	mainmenu = widgets.yawTtk.Menu(menubar, tearoff=False, name="mainmenu")
	networkmenu = widgets.yawTtk.Menu(menubar, tearoff=False, name="networkmenu")
	for net in util.findNetworks():
		networkmenu.add("radiobutton", variable="ui.network", label=net, value=net, command=lambda n=net:useNetwork(n))
	networkmenu.invoke(0)
	mainmenu.add("cascade", ulabel="_Network", menu=networkmenu)
	mainmenu.add("separator")
	mainmenu.add("command", compound="left", image=_exit, ulabel="_Close", command=exit)
	menubar.add("cascade", ulabel="_Pool", menu=mainmenu)
	toplevel.configure(menu=menubar)

	toplevel.protocol('WM_DELETE_WINDOW', exit)
	toplevel.minsize(450, int(450*1.618033989))
	toplevel.maxsize(450, int(450*1.618033989))
	toplevel.resizable(False, False)
	toplevel.deiconify()
	__heartbeat = heartBeat()
	toplevel.mainloop()

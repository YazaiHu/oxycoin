# -*- encoding: utf8 -*-
# © Toons

from .. import __PY3__, api, cfg, util, crypto
from ..cli import share
from . import ROOT

import io, os, sys, json, time, yawTtk, webbrowser


class DataView(yawTtk.Tree):

	def __init__(self, parent=None, cnf={}, **kw):
		yawTtk.Tree.__init__(self, parent, cnf, **kw)
		self.tag_configure("even", background="lavender")
		self.tag_configure("odd", background="lightblue")
		self.tag_configure("treating", background="steelblue", foreground="white")
		self.tag_configure("okay", background="lightgreen")
		self.tag_configure("error", background="red", foreground="white")
		self.rows = []
		self.headers = []
		self.__data_headings = []
		self.__sort_meaning = "ASC"
		self.configureHeader()

	def configureHeader(self):
		self.__data_headings = self.headers if len(self.headers) else \
		                       list(self.rows[0].keys()) if len(self.rows) else \
		                       []
		self['columns'] = " ".join(["{%s}"%h for h in self.__data_headings])
		for i in range(len(self.__data_headings)):
			text = self.__data_headings[i]
			self.heading("#%d"%(i+1), text=text, command=lambda o=self,k=text: o.populate(k,None))
			self.column("#%d"%(i+1), anchor="center", stretch=1)

	def populate(self, sortkey=None, meaning=None):
		# clear data
		self.delete(*self.xchildren())
		if not len(self.rows):
			return
		# check witch meaning use
		if meaning == None:
			meaning = "ASC" if self.__sort_meaning == "DESC" else "DESC"
		self.__sort_meaning = meaning
		# sort data if asked
		if sortkey != None:
			rows = sorted(self.rows, key=lambda e:e.get(sortkey, ""), reverse=False if meaning == "ASC" else True)
		else:
			rows = self.rows
		# populate data
		even=False
		for row in rows:
			self.insert(value=tuple(row.get(k, "") for k in self.headers), tag=("even",) if even else ("odd",))
			even = not even


class AddressPanel(yawTtk.Frame):

	address = None
	status = {}
	voters = []

	def __init__(self, master=None, cnf={}, **kw):
		self._bank=\
"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH4QgVAgk3LIBEwwAAASxJREFUOMutkjtOA0EQRF+Vd8ESRoQQIFJO"\
"wwGQA45BSAwS5+ASXIIEB0RkSBBhsEE2PQT0ovFHBMBIo+7tramZri5Ys2zJlqtv29JabAXC/sJElALs27qxNQIOsvaN67D1jW3mx7YebJWl/WjrJDFtnlkgObc1TvBsDUFXm9i66NqUrT4wBWZAL9sKQLkBSu7u"\
"3wfQRhQ1QJOgttKmZKwJIgm8oB0wAbaBe2AO3AJbwLAiHEaUFrhOoldgt54Uti6zxzNbTdbmtp4zH9g6SszVyhiBzYwb2WPXgvOmOdCvMCsEv1r/SjCtYlOrH1Ein/2S9TeWfL6XBnm39WRrJ8XsTHSa9r1LYYut"\
"Q1s9JUmpzEPm9QujErXDKKJItsbL5sin6wdjkVMZ/FVDPgFDQFnymyipTAAAAABJRU5ErkJggg=="
		self._shield=\
"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH4QgVAgYa7scEeQAAAPxJREFUOMuV0j1KBEEQhuFnmlnN/MHARBET"\
"U6MNxRN4AwND8Qbew0jEC2ikCF7BGxhrKqIG7vo3Y1ILvcv2jn5QdHdR9XZVdVfGlbCFPaxhET284BFXuEdjhq7xjDtcYogPvONWh/poJ3yDuLEN65tS9jreIuAA1QxAi1dsItURvBS9VmFtR6ULkfOQwlHhK/Zd"\
"ySM1o/LhE3UhsC1AB/kMVmfc3BZsBSnvuQSoCtAKVcoSfwqQuQySsJyDUna4wHfH4Grs42baX9go9DqqoM7K3y4N/SRrJQfMB+QJ513vexqJTTaTo9if/fGP2M0Aw7Ad/1Av1mMcTvjG9AuKU0sA0hz6OAAAAABJ"\
"RU5ErkJggg=="
		self._cloud=\
"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH4QgVAhwTJzZGBgAAAZxJREFUOMvFUz1Lm1EUfp5z33yQ2JhqJQ2C"\
"2imQpWMHhxQShQQydXBw6OqigoMurp06tP+ii+DgkKEIUigOKejSqeigIEhtiZBi4k3ucfC+8hICbejggQOHwznPx7lc4D+DlcprAEAymUSj8RmqiiAIsLW1hsPDbyOBGQCM1PJPCmq1RdNut6XZPJrtdjurqiiQ"\
"PMpkUu9brfbv6HCxWEjMzc30bm9tSKTil2c6nc4PVawAqKjqxvX1n18isklSSaqINC4vfybK5ZJa+wAgBACSXQCxiAUA6HsrfW+HAG6CIFiw1n6tVhdi1lpFOp3OexYXsvk8873vkV7Pqzk4Pv7C+flXAfL5508i"\
"AI6kxuOJQjY7/tQYs+0VnpC0UYLJyYlMvV6NYWpqIjtEwXnoQ0TWB5SFsxe53LMxiMinyLIjqcaY5RAglUpNkzwdVOBzXwC8jByPAOCcKxtj3pI86/VsDsALf9DBKEFE3pHsD0H/a4rIRy4tvTE7O7vrzmkdgJKk"\
"qhKA8zXu+xBVaDgDYO/q6uQDBt5+5L+ER487awatf6VW7KoAAAAASUVORK5CYII="
		yawTtk.Frame.__init__(self, master, cnf={}, **kw)
		self.columnconfigure(0, minsize=160)
		self.columnconfigure(1, weight=1, minsize=70)
		self.columnconfigure(2, minsize=120)

		self.wallet = yawTtk.StringVar(self, "", "%s.wallet"%self._w)
		self.balance = yawTtk.StringVar(self, "", "%s.balance"%self._w)

		yawTtk.Label(self, font=("tahoma", "8", "bold"), text="Address").grid(row=0, column=0, columnspan=2, sticky="nesw", padx=4, pady=4)
		self.combo = yawTtk.Combobox(self, width=-1, textvariable=self.wallet).grid(row=1, column=0, sticky="nesw", padx=4, pady=4)
		self.label = yawTtk.Label(self, cursor="hand2", relief="solid", padding=(5,0), compound="image", image=self._cloud).grid(row=1, column=1, sticky="nsw", pady=4)
		yawTtk.Entry(self, font=("courrier-new", "8", "bold"), state="readonly", justify="right", textvariable=self.balance).grid(row=1, column=2, sticky="nes", padx=4, pady=4)
		self.label.bind("<Button-1>", lambda e:webbrowser.open(cfg.explorer+"/address/"+self.wallet.get()))

	def update(self, *args, **kw):
		value = self.wallet.get().strip()
		# exit if wallet value is didn't change
		if value == AddressPanel.address: return
		# if value changed, store it...
		AddressPanel.address = value
		# ... ask oxycoin blockchain ...
		AddressPanel.status = api.GET.accounts(address=value)
		# ... and check if it is a valid address
		if AddressPanel.status["success"]:
			# if valid addres, get status info
			AddressPanel.status = AddressPanel.status["account"]
			# try to merge it with delegate info if this address is a delegate address
			AddressPanel.status.update(api.GET.delegates.get(publicKey=AddressPanel.status["publicKey"]).get("delegate", {}))
			# update balance
			self.balance.set("%s %.8f" % (cfg.symbol, float(AddressPanel.status["balance"])/100000000.0))
			if AddressPanel.status.get("username", False):
				# if username found, then it is a delegate address, get voters
				AddressPanel.voters = api.GET.delegates.voters(publicKey=AddressPanel.status["publicKey"], returnKey="accounts")
				# put delegate icon and set backround according to delegate rate (forge or relay) and update text value
				self.label.configure(
					image = self._shield,
					background = "lightgreen" if AddressPanel.status["rate"] <= 201 else "yellow3",
					compound = "left",
					text = "#%(rate)s - %(username)s" % AddressPanel.status
				)
			else:
				# else, put a bank icon and hide text
				AddressPanel.voters = []
				self.label.configure(
					image = self._bank,
					background = "steelblue",
					compound = "image"
				)
		else:
			# else, put a cloud icon, hide text and reset data
			self.balance.set("")
			AddressPanel.status = {}
			AddressPanel.voters = []
			self.label.configure(
				image = self._cloud,
				background = self["background"], #"SystemButtonFace",
				compound = "image"
			)

	def getAddress(self):
		return AddressPanel.status.get("address", False)

	def getDelegate(self):
		return AddressPanel.status.get("username", False)

	def getVotes(self):
		return dict((voter["address"], float(voter["balance"])/100000000.) for voter in AddressPanel.voters)

	def getBalance(self):
		try: return float(AddressPanel.status.get("balance", False))/100000000.
		except: return False


class OptionPannel(yawTtk.Frame):

	options = {}

	def __init__(self, master=None, cnf={}, **kw):
		yawTtk.Frame.__init__(self, master, cnf={}, **kw)
		self.columnconfigure(1, weight=1)

		self.delay = yawTtk.StringVar(self, "%s"%OptionPannel.options.get("delay", 7), "%s.delay"%self._w)
		self.lowest = yawTtk.StringVar(self, "%s"%OptionPannel.options.get("lowest", (cfg.fees["send"]/100000000)), "%s.lowest"%self._w)
		self.highest = yawTtk.StringVar(self, "%s"%OptionPannel.options.get("highest", None), "%s.highest"%self._w)
		yawTtk.Label(self, font=("tahoma", "8", "bold"), text="Options").grid(row=0, column=0, columnspan=2, sticky="nsw", padx=4, pady=4)
		yawTtk.Label(self, padding=(0,0,2,0), text="Delay in days").grid(row=1, column=0, sticky="new", padx=4)
		yawTtk.Entry(self, font=("tahoma", "10"), padding=(2,0), relief="flat", textvariable=self.delay).grid(row=1, pady=1, column=1, sticky="w", padx=4).bind("<FocusOut>", lambda e,k="delay",d=7: self.updateValue(e,k,d))
		yawTtk.Label(self, padding=(0,0,2,0), text="Minimum payout").grid(row=2, column=0, sticky="new", padx=4)
		yawTtk.Entry(self, font=("tahoma", "10"), padding=(2,0), relief="flat", textvariable=self.lowest).grid(row=2, pady=1, column=1, sticky="w", padx=4).bind("<FocusOut>", lambda e,k="lowest",d=0.1: self.updateValue(e,k,d))
		yawTtk.Label(self, padding=(0,0,2,0), text="Maximum payout").grid(row=3, column=0, sticky="new", padx=4)
		yawTtk.Entry(self, font=("tahoma", "10"), padding=(2,0), relief="flat", textvariable=self.highest).grid(row=3, pady=1, column=1, sticky="w", padx=4).bind("<FocusOut>", lambda e,k="highest",d=None: self.updateValue(e,k,d))
		yawTtk.Label(self, padding=(0,0,2,0), text="Blacklisted addresses").grid(row=4, column=0, sticky="new", padx=4)
		self.blacklist = yawTtk.Tkinter.Text(self, font=("tahoma", "10"), width=0, height=3, border=0, highlightthickness=1, highlightbackground="grey", highlightcolor="steelblue", relief="solid", wrap="word")
		self.blacklist.bind("<FocusOut>", self.updateList)
		self.blacklist.grid(row=4, pady=1, column=1, sticky="nesw", padx=4)
		self.blacklist.insert("1.0", ",".join(OptionPannel.options.get("blacklist", [])))

	def loadConf(self):
		self.blacklist.delete("1.0", "end")
		OptionPannel.options = util.loadJson("%s-%s.json" % (cfg.network, AddressPanel.status.get("username", "config")))
		self.delay.set("%s"%OptionPannel.options.get("delay", 7))
		self.lowest.set("%s"%OptionPannel.options.get("lowest", (cfg.fees["send"]/100000000)))
		self.highest.set("%s"%OptionPannel.options.get("highest", None))
		self.blacklist.insert("1.0", ",".join(OptionPannel.options.get("blacklist", [])))

	def saveConf(self):
		util.dumpJson(OptionPannel.options, "%s-%s.json" % (cfg.network, AddressPanel.status.get("username", "config")))

	def updateValue(self, event, key, default):
		value = event.widget.get().strip()
		try: value = default if value == "" else int(value)
		except: value = default
		OptionPannel.options[key] = value
		event.widget.delete(0,"end")
		event.widget.insert(0, "%s" % value)

	def updateList(self, event):
		value = self.blacklist.get("1.0", "end-1c").strip()
		value = value.replace("\n", ",").replace(" ", ",").replace("\t", ",")
		OptionPannel.options["blacklist"] = [a.strip() for a in value.split(",") if a != ""]
		self.blacklist.delete("1.0", "end")
		self.blacklist.insert("1.0", ",".join(OptionPannel.options["blacklist"]))

	def disable(self):
		for widget in self.children.values():
			if isinstance(widget, yawTtk.Entry):
				widget.state("disabled")
			self.blacklist["state"] = "disabled"

	def enable(self):
		for widget in self.children.values():
			if isinstance(widget, yawTtk.Entry):
				widget.state("!disabled")
			self.blacklist["state"] = "normal"

	def destroy(self):
		self.saveConf()
		yawTtk.Frame.destroy(self)


class ShareFrame(yawTtk.Frame):

	satoshi = 0

	def __init__(self, master=None, cnf={}, **kw):
		yawTtk.Frame.__init__(self, master, cnf={}, **kw)
		self.columnconfigure(0, minsize=160)
		self.columnconfigure(1, weight=1, minsize=60)
		self.columnconfigure(2, minsize=120)

		self.amount = yawTtk.DoubleVar(self, 0., "%s.amount"%self._w)
		self.value = yawTtk.StringVar(self, "%s 0.00000000" % cfg.symbol, "%s.value"%self._w)
		self.what = yawTtk.StringVar(self, cfg.symbol, "%s.what"%self._w)
		self.satoshi = 0

		yawTtk.Label(self, font=("tahoma", "8", "bold"), text="Share").grid(row=0, column=0, columnspan=3, sticky="nesw", padx=4, pady=4)
		yawTtk.Entry(self, width=-1, textvariable=self.amount, justify="right").grid(row=1, column=0, sticky="nesw", padx=4, pady=4)
		self.combo = yawTtk.Combobox(self, textvariable=self.what, state="readonly", values=(cfg.symbol, "$", "€", "£", "¥", "%"), width=5).grid(row=1, column=1, pady=4, sticky="nsw")
		yawTtk.Entry(self, font=("courrier-new", "8", "bold"), state="readonly", justify="right", textvariable=self.value).grid(row=1, column=2, sticky="nesw", padx=4, pady=4)

		self.amount.trace("w", self.update)
		self.what.trace("w", self.update)

	def update(self, *args, **kw):
		what = self.what.get()
		try:
			amount = self.amount.get()
		except:
			value = 0.
		else:
			if what == "%":
				value = (float(AddressPanel.status.get("balance", 0))*amount/100 - cfg.fees["send"])/100000000.
			elif what in ["$", "€", "£", "¥"]:
				price = util.getTokenPrice(cfg.token, {"$":"usd", "€":"eur", "£":"gbp", "¥":"cny"}[what])
				value = amount / price
			else:
				value = amount
		# finally:
		ShareFrame.satoshi = 100000000.*max(0., value)
		self.value.set("%s %.8f" % (cfg.symbol, value))

	def get(self):
		return ShareFrame.satoshi


class Secret(yawTtk.Frame):

	def __init__(self, master=None, cnf={}, **kw):
		yawTtk.Frame.__init__(self, master, cnf={}, **kw)
		self["relief"] = "flat"
		border = self["border"]
		border = 1 if border == "" else int(border)
		self.rowconfigure(0, weight=1)
		self.columnconfigure(0, weight=1)
		self.rowconfigure(1, minsize=border)

		self.secret = yawTtk.Tkinter.Text(self, font=("tahoma", "10"), width=0, height=2, border=2, highlightthickness=1, highlightbackground="grey", highlightcolor="steelblue", relief="flat", wrap="word")
		self.secret.grid(row=0, column=0, sticky="nesw", padx=4)
		self.border = yawTtk.Frame(self).grid(row=1, column=0, sticky="nesw", padx=4)
		self.border["background"] = "steelblue"


class SecretFrame(yawTtk.Frame):

	secret = None
	secondSecret = None

	def __init__(self, master=None, cnf={}, **kw):
		yawTtk.Frame.__init__(self, master, cnf={}, **kw)
		self.columnconfigure(1, weight=1)

		yawTtk.Label(self, font=("tahoma", "8", "bold"), text="Secrets").grid(row=0, column=0, columnspan=2, sticky="nesw", padx=4, pady=4)
		yawTtk.Label(self, padding=(0,0,2,0), text="First").grid(row=1, column=0, sticky="new", padx=4)
		self.first = Secret(self).grid(row=1, column=1, sticky="nesw", pady=4)
		self.label = yawTtk.Label(self, padding=(0,0,2,0), text="Second")
		self.second = Secret(self)

	def update(self):
		secret = self.first.secret.get("1.0", "end-1c")
		if crypto.getKeys(secret)[0] == AddressPanel.status.get("publicKey", ""):
			SecretFrame.secret = secret
			self.first.border["background"] = "lightgreen"
		else:
			SecretFrame.secret = None
			self.first.border["background"] = "red"
		self.first.secret["highlightbackground"] = self.first.border["background"]

		if AddressPanel.status.get("secondPublicKey", False):
			self.second.grid(row=2, column=1, sticky="nesw", pady=4)
			self.label.grid(row=2, column=0, sticky="new", padx=4)
			self.first.grid_configure(pady=0)
			secondSecret = self.second.secret.get("1.0", "end-1c")
			if crypto.getKeys(secondSecret)[0] == AddressPanel.status.get("secondPublicKey", ""):
				SecretFrame.secondSecret = secondSecret
				self.second.border["background"] = "lightgreen"
			else:
				SecretFrame.secondSecret = None
				self.second.border["background"] = "red"
			self.second.secret["highlightbackground"] = self.second.border["background"]
		else:
			self.second.grid_forget()
			self.label.grid_forget()
			self.first.grid_configure(pady=4)
			self.second.border["background"] = self.first.border["background"]
			self.second.secret["highlightbackground"] = self.first.border["background"]

	def check(self):
		return True if self.first.border["background"] == self.second.border["background"] == "lightgreen" else False


class PayoutFrame(yawTtk.Frame):

	voterforces = {}
	busy = False

	def __init__(self, master=None, cnf={}, **kw):
		yawTtk.Frame.__init__(self, master, cnf={}, **kw)
		self.columnconfigure(0, weight=1)
		self.rowconfigure(1, weight=1)

		yawTtk.Label(self, font=("tahoma", "8", "bold"), text="Payroll").grid(row=0, column=0, sticky="nesw", padx=4, pady=4)
		frame = yawTtk.Frame(self, border=0, padding=4, height=0).grid(row=1, column=0, columnspan=2, sticky="nesw")
		frame.columnconfigure(0, weight=1)
		frame.rowconfigure(0, weight=1)
		self.data = DataView(frame, padding=0, height=0, show="headings").grid(row=0, column=0, sticky="nesw")
		self.data.headers = ["address", "payout", "weight (%)", "send", "saved"]
		self.data.configureHeader()
		yawTtk.Autoscrollbar(frame, target=self.data, orient="horizontal").grid(row=1, column=0, sticky="nesw")
		yawTtk.Autoscrollbar(frame, target=self.data, orient="vertical").grid(row=0, column=1, rowspan=2, sticky="nesw")

	def analyse(self):
		PayoutFrame.busy = True
		self.data.rows = []
		self.data.populate()
		delay = OptionPannel.options.get("delay", 7)
		PayoutFrame.voterforces = dict([address, util.getVoteForce(address, days=delay)] for address in [v["address"] for v in AddressPanel.voters])
		PayoutFrame.busy = False

	def compute(self):
		amount = ShareFrame.satoshi
		maximum = OptionPannel.options.get("highest", None)
		blacklist = OptionPannel.options.get("blacklist", [])
		voterforces =  dict([a,f] for a,f in PayoutFrame.voterforces.items() if a not in blacklist)
		if maximum:
			contribution = share.ceilContribution(voterforces, sum(voterforces.values())*maximum*100000000/amount)
			return share.normContribution(contribution).items()
		return share.normContribution(voterforces).items()

	def update(self):
		PayoutFrame.busy = True
		payroll = ShareFrame.satoshi

		self.data.rows = []
		if payroll > 100000000:
			minimum = OptionPannel.options.get("lowest", cfg.fees["send"]/100000000)*100000000
			saved_payout = util.loadJson("%s-%s.rnd" % (cfg.network, AddressPanel.status.get("username", "")))

			for address, weight in self.compute():
				saved = saved_payout.get(address, 0.)
				payout = payroll * weight + saved*100000000 - cfg.fees["send"]
				row = {"address":address, "weight (%)":round(weight*100,2), "payout":round(payout/100000000, 8), "send":"Yes", "saved":saved}
				if payout > minimum:
					saved_payout.pop(address, None)
					self.data.rows.append(row)
				elif payout + cfg.fees["send"] > 0:
					saved_payout[address] = payout + cfg.fees["send"]
					row["send"] = "No"
					row["payout"] = round(saved_payout[address]/100000000, 8)
					self.data.rows.append(row)
		self.data.populate(sortkey="weight (%)", meaning="DESC")
		PayoutFrame.busy = False

	def broadcast(self):
		if not PayoutFrame.busy:
			PayoutFrame.busy = True
			to_save = {}
			for elem in self.data.walk(''):
				self.data.see(elem)
				self.data.item(elem, tags=("treating"))
				row = self.data.set(elem)
				if row["send"] == "Yes":
					payload = crypto.bakeTransaction(
						amount=row["payout"]*100000000,
						publicKey=crypto.getKeys(SecretFrame.secret)[0],
						secret=SecretFrame.secret,
						secondSecret=SecretFrame.secondSecret,
						recipientId=row["address"]
					)
					resp = api.post("/peer/transactions", transactions=[payload])
					if resp["success"]:
						self.data.item(elem, tags=("okay"))
						self.data.set(elem, "send", "OK")
					else:
						self.data.item(elem, tags=("error"))
						self.data.set(elem, "send", "ERROR")
				elif row["send"] == "No":
					to_save[row["address"]] = row["payout"]
					self.data.set(elem, "send", "SAVED")
			if len(to_save):
				util.dumpJson(to_save,"%s-%s.rnd" % (cfg.network, AddressPanel.status.get("username", "")))
			PayoutFrame.busy = False

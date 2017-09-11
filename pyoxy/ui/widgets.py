# -*- encoding: utf8 -*-
# © Toons

from .. import api, cfg, util, crypto

import sys, yawTtk, webbrowser


class DataView(yawTtk.Tree):

	def __init__(self, parent=None, cnf={}, **kw):
		yawTtk.Tree.__init__(self, parent, cnf, **kw)
		self.tag_configure("even", background="lavender")
		self.tag_configure("odd", background="lightblue")
		self.rows = []
		self.headers = []
		self.__data_headings = []
		self.__sort_meaning = "ASC"
		self.configureHeader()

	def configureHeader(self):
		self.__data_headings = self.headers if len(self.headers) else \
		                       list(rows[0].keys()) if len(self.rows) else \
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
			rows = sorted(self.rows, key=lambda e:e.get(sortkey, ""), reverse=True if meaning == "ASC" else False)
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
		self.columnconfigure(3, weight=1)

		self.wallet = yawTtk.StringVar(self, "", "%s.wallet"%self._w)
		self.balance = yawTtk.StringVar(self, "", "%s.balance"%self._w)

		yawTtk.Label(self, font=("tahoma", "8", "bold"), text="Wallet address").grid(row=0, column=0, sticky="nesw", padx=4, pady=4)
		self.combo = yawTtk.Combobox(self, width=28, font=("courrier-new", "8", "bold"), textvariable=self.wallet).grid(row=0, column=1, sticky="nesw", padx=4, pady=4)
		yawTtk.Entry(self, font=("courrier-new", "8", "bold"), state="readonly", justify="right", textvariable=self.balance).grid(row=0, column=2, sticky="nesw", pady=4)
		self.label = yawTtk.Label(self, cursor="hand2", relief="solid", padding=(5,0), compound="image", image=self._cloud).grid(row=0, column=3, sticky="nes", padx=4, pady=4)
		self.label.bind("<Button-1>", lambda e:webbrowser.open(cfg.explorer+"/address/"+self.wallet.get()))

		# this line enable to launch an infinite threaded loop for widget update
		@util.setInterval(2)
		def _update(obj):
			obj.update()
		# __stop_update is an Event to set so it stop infinite loop
		self.__stop_update = _update(self)

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
				background = "SystemButtonFace",
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

	def destroy(self):
		self.__stop_update.set()
		yawTtk.Frame.destroy(self)


class SharePannel(yawTtk.Frame):

	def __init__(self, master=None, cnf={}, **kw):
		yawTtk.Frame.__init__(self, master, cnf={}, **kw)
		self.columnconfigure(1, weight=1)

		self.delay = yawTtk.IntVar(self, 7, "%s.delay"%self._w)
		self.lowest = yawTtk.StringVar(self, "", "%s.lowest"%self._w)
		self.highest = yawTtk.StringVar(self, "", "%s.highest"%self._w)

		yawTtk.Label(self, font=("tahoma", "8", "bold"), text="Share options").grid(row=0, column=0, columnspan=2, sticky="nsw", padx=4, pady=4)
		yawTtk.Label(self, padding=(0,0,2,0), text="Delay in days").grid(row=1, column=0, sticky="new", padx=4)
		yawTtk.Entry(self, font=("tahoma", "10"), padding=(2,0), relief="flat", textvariable=self.delay).grid(row=1, pady=1, column=1, sticky="w", padx=4)
		yawTtk.Label(self, padding=(0,0,2,0), text="Minimum payout").grid(row=2, column=0, sticky="new", padx=4)
		yawTtk.Entry(self, font=("tahoma", "10"), padding=(2,0), relief="flat", textvariable=self.lowest).grid(row=2, pady=1, column=1, sticky="w", padx=4)
		yawTtk.Label(self, padding=(0,0,2,0), text="Maximum payout").grid(row=3, column=0, sticky="new", padx=4)
		yawTtk.Entry(self, font=("tahoma", "10"), padding=(2,0), relief="flat", textvariable=self.highest).grid(row=3, pady=1, column=1, sticky="w", padx=4)
		yawTtk.Label(self, padding=(0,0,2,0), text="Blacklisted addresses").grid(row=4, column=0, sticky="new", padx=4)
		self.blacklist = yawTtk.Tkinter.Text(self, font=("tahoma", "10"), width=0, height=3, border=0, highlightthickness=1, highlightbackground="grey", highlightcolor="SystemHighLight", relief="solid", wrap="word")
		self.blacklist.grid(row=4, pady=1, column=1, sticky="nesw", padx=4)


class AmountFrame(yawTtk.Frame):

	def __init__(self, master=None, cnf={}, **kw):
		yawTtk.Frame.__init__(self, master, cnf={}, **kw)
		self.columnconfigure(0, weight=1)
		self.columnconfigure(1, weight=0, minsize=50)
		self.columnconfigure(2, weight=0, minsize=120)

		self.amount = yawTtk.DoubleVar(self, 0., "%s.amount"%self._w)
		self.value = yawTtk.StringVar(self, "%s 0.00000000" % cfg.symbol, "%s.value"%self._w)
		self.what = yawTtk.StringVar(self, cfg.symbol, "%s.what"%self._w)
		self.satoshi = 0

		yawTtk.Label(self, padding=2, text="amount", background="lightgreen", font=("tahoma", 8, "bold")).grid(row=0, column=0, columnspan=3, pady=4, sticky="nesw")
		yawTtk.Entry(self, textvariable=self.amount, justify="right").grid(row=1, column=0, pady=4, sticky="nesw")
		yawTtk.Combobox(self, textvariable=self.what, state="readonly", values=(cfg.symbol, "$", "€", "£", "¥", "%"), width=-1).grid(row=1, column=1, padx=4, pady=4, sticky="nesw")
		yawTtk.Label(self, textvariable=self.value, relief="solid").grid(row=1, column=2, pady=4, sticky="nesw")

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
		finally:
			self.satoshi = 100000000.*max(0., value)
			self.value.set("%s %.8f" % (cfg.symbol, value))

	def get(self):
		return self.satoshi


class SecretFrame(yawTtk.Frame):

	def __init__(self, master=None, cnf={}, **kw):
		yawTtk.Frame.__init__(self, master, cnf={}, **kw)
		self["relief"] = "flat"
		border = self["border"]
		border = 1 if border == "" else int(border)
		self.rowconfigure(0, weight=1)
		self.columnconfigure(0, weight=1)
		self.rowconfigure(1, minsize=border)

		self.secret = yawTtk.Tkinter.Text(self, font=("tahoma", "10"), width=0, height=2, border=2, highlightthickness=1, highlightbackground="grey", highlightcolor="SystemHighLight", relief="flat", wrap="word")
		self.secret.grid(row=0, column=0, sticky="nesw", padx=4)
		self.border = yawTtk.Frame(self, background="SystemHighLight").grid(row=1, column=0, sticky="nesw", padx=4)

		# this line enable to launch an infinite threaded loop for widget update
		@util.setInterval(2)
		def _update(obj):
			obj.update()
		# __stop_update is an Event to set so it stop infinite loop
		self.__stop_update = _update(self)
		self.update()

	def getKeys(self):
		return crypto.getKeys(self.secret.get("1.0", "end-1c"))

	def update(self):
		self.border["background"] = "lightgreen" if self.getKeys()[0] == AddressPanel.status.get("publicKey", "") else "red"
		self.secret["highlightbackground"] = self.border["background"]

	def check(self):
		return True if self.border["background"] == "lightgreen" else False

	def destroy(self):
		self.__stop_update.set()
		yawTtk.Frame.destroy(self)

# -*- encoding: utf8 -*-
# © Toons

from . import __PY3__, __FROZEN__, ROOT
if not __PY3__: import api, cfg, slots, crypto
else: from . import api, cfg, slots, crypto

import sys, logging, threading

def setInterval(interval):
	""" threaded decorator
>>> @setInterval(10)
... def tick(): print("Tick")
>>> stop = tick() # print 'Tick' every 10 sec
>>> type(stop)
<class 'threading.Event'>
>>> stop.set() # stop printing 'Tick' every 10 sec
"""
	def decorator(function):
		def wrapper(*args, **kwargs):
			stopped = threading.Event()
			def loop(): # executed in another thread
				while not stopped.wait(interval): # until stopped
					function(*args, **kwargs)
			t = threading.Thread(target=loop)
			t.daemon = True # stop if the program exits
			t.start()
			return stopped
		return wrapper
	return decorator

def prettyfy(dic, tab="    "):
	result = ""
	if len(dic):
		maxlen = max([len(e) for e in dic.keys()])
		for k,v in dic.items():
			if isinstance(v, dict):
				result += tab + "%s:" % k.ljust(maxlen)
				result += prettyfy(v, tab*2)
			else:
				result += tab + "%s: %s" % (k.rjust(maxlen),v)
			result += "\n"
		return result

def prettyPrint(dic, tab="    ", log=True):
	pretty = prettyfy(dic, tab)
	if len(dic):
		sys.stdout.write(pretty)
		if log: logging.info("\n"+pretty.rstrip())
	else:
		sys.stdout.write("Nothing to print here\n")
		if log: logging.info("Nothing to log here")

def askYesOrNo(msg):
	answer = ""
	while answer not in ["y", "Y", "n", "N"]:
		answer = input("%s [y-n]> " % msg)
	return False if answer in ["n", "N"] else True

def floatAmount(amount, address):
	if amount.endswith("%"):
		return (float(amount[:-1])/100 * float(api.GET.accounts.getBalance(address=address, returnKey="balance")) - cfg.fees["send"])/100000000.
	elif amount[0] in ["$", "€", "£", "¥"]:
		price = api.getTokenPrice(cfg.token, {"$":"usd", "EUR":"eur", "€":"eur", "£":"gbp", "¥":"cny"}[amount[0]])
		result = float(amount[1:])/price
		if askYesOrNo("%s=%s%f (%s/%s=%f) - Validate ?" % (amount, cfg.token, result, cfg.token, amount[0], price)):
			return result
		else:
			return False
	else:
		return float(amount)

def unlockAccount(address, secret, secondSecret=None):
	if crypto.getAddress(crypto.unhexlify(crypto.getKeys(secret)[0])) == address:
		account = api.GET.accounts(address=address)
		if account["success"]:
			account = account["account"]
			if account["secondSignature"]:
				if not secondSecret: input("Enter your second secret : ")
				return crypto.getKeys(secondSecret)[0] == account["secondPublicKey"]
			else:
				return True
		else:
			return True
	else:
		return False

def sendTransaction(**kw):
	return api.post("/peer/transactions", transactions=[crypto.bakeTransaction(**kw)])

def getTransactions(timestamp=0, **param):
	param.update(returnKey="transactions", limit=1000, orderBy="timestamp:desc")
	txs = api.GET.transactions(**param)
	if isinstance(txs, list) and len(txs):
		while txs[-1]["timestamp"] >= timestamp:
			param.update(offset=len(txs))
			search = api.GET.transactions(**param)
			txs.extend(search)
			if len(search) < 1000:
				break
	elif not len(txs):
		raise Exception("Address has null transactions.")
	else:
		raise Exception(txs.get("error", "Api error"))
	return sorted([t for t in txs if t["timestamp"] >= timestamp], key=lambda e:e["timestamp"], reverse=True)

def getHistory(address, timestamp=0):
	return getTransactions(timestamp, recipientId=address, senderId=address)

def getVoteForce(address, **kw):
	# determine timestamp
	now = slots.datetime.datetime.now(slots.pytz.UTC)
	delta = slots.datetime.timedelta(**kw)
	timestamp_limit = slots.getTime(now - delta)
	# get actual balance and transaction history
	balance = float(api.GET.accounts.getBalance(address=address, returnKey="balance"))/100000000.
	history = getHistory(address, timestamp_limit)
	# if no transaction over periode integrate balance over delay and return it
	if not history:
		return balance*max(1./3600, delta.total_seconds()/3600)
	# else
	end = slots.getTime(now)
	sum_ = 0.
	brk = False
	for tx in history:
		delta_t = (end - tx["timestamp"])/3600
		sum_ += balance * delta_t
		balance += ((tx["fee"]+tx["amount"]) if tx["senderId"] == address else -tx["amount"])/100000000.
		if tx["type"] == 3:
			brk = True
			break
		end = tx["timestamp"]
	if not brk:
		sum_ += balance * (end - timestamp_limit)/3600
	return sum_

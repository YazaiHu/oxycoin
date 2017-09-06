# -*- encoding: utf8 -*-
# © Toons

'''
Usage: share <username> <amount> [-c -b <blacklist> -d <delay> -l <lowest> -h <highest>]

Options:
-b <blacklist> --blacklist <blacklist> account addresses to exclude (comma-separated list or pathfile)
-h <highest> --highest <hihgest>       maximum payout during payroll
-l <lowest> --lowest <lowest>          minimum payout during payroll
-d <delay> --delay <delay>             number of fidelity-day [default: 30]
-c --complement                        share the amount complement
'''

from . import __PY3__, __FROZEN__, ROOT
if not __PY3__: import api, cfg, util
else: from . import api, cfg, util

import os, io, sys, json, shlex, docopt, collections

def getopt(line):
	argv = shlex.split(line)
	if len(argv) and argv[0] == "share":
		try:
			return docopt.docopt(__doc__, argv=argv[1:])
		except:
			sys.stdout.write("%s\n" % __doc__.strip())
			return {}

def dumpRound(round, name):
	filename = os.path.join(ROOT, name)
	out = io.open(filename, "w" if __PY3__ else "wb")
	json.dump(round, out, indent=2)
	out.close()
	return os.path.basename(filename)

def loadRound(name):
	filename = os.path.join(ROOT, name)
	if os.path.exists(filename):
		in_ = io.open(filename, "r" if __PY3__ else "rb")
		round_ = json.load(in_)
		in_.close()
		return round_
	else:
		return {}

def getContribution(username, *excludes, **kw):
	delegate = api.GET.delegates.get(username=username)
	if delegate["success"]: delegate = delegate["delegate"]
	else: return {}

	voters = api.GET.delegates.voters(publicKey=delegate["publicKey"], returnKey="accounts")
	return dict([address, util.getVoteForce(address, **kw)] for address in [voter["address"] for voter in voters] if address not in excludes)

def ceilContribution(contribution, ceil):
	cumul = 0
	# first filter
	for address,force in [(a,f) for a,f in contribution.items() if f >= ceil]:
		contribution[address] = ceil
		cumul += force - ceil
	# report cutted share
	untouched_pairs = sorted([(a,f) for a,f in contribution.items() if f < ceil], key=lambda e:e[-1], reverse=True)
	n, i = len(untouched_pairs), 0
	bounty = cumul / max(1, n)
	for address,force in untouched_pairs:
		if force + bounty > ceil:
			i += 1
			n -= 1
			contribution[address] = ceil
			bounty = (cumul - abs(ceil - force)) / n
		else:
			break
	for address,force in untouched_pairs[i:]:
		contribution[address] += bounty

	return contribution

def normContribution(contribution):
	k = 1.0/sum(contribution.values())
	return dict((a, s*k) for a,s in contribution.items())



# def getContribution(param, secret=None, secondSecret=None):
	# delegate = api.Delegate.getDelegate(param["<username>"], returnKey="delegate") 
	# if "username" not in delegate:
	# 	sys.stdout.write("%s is not a valid delegate name !" % param["<username>"])
	# 	return False
	# account = api.Account.getAccount(delegate.get("address"), returnKey="account")

	# if not unlockAccount(secret, account.get("publicKey"), secondSecret, account.get("secondPublicKey")):
 # 		return False

	# if param["--blacklist"]:
	# 	if os.path.exists(param["--blacklist"]):
	# 		with io.open(param["--blacklist"], "r") as in_:
	# 			blacklist = [e for e in in_.read().split() if e != ""]
	# 	else:
	# 		blacklist = param["--blacklist"].split(",")
	# else:
	# 	blacklist = []

	# balance = float(api.Account.getBalance(delegate.get("address"), returnKey="balance"))
	# amount = floatAmount(param["<amount>"], delegate.get("address"))
	# if param["--complement"]:
	# 	amount = balance/100000000. - amount

	# if param["--lowest"] : minimum = float(param["--lowest"])
	# else: minimum = 0.

	# if param["--highest"] : maximum = float(param["--highest"])
	# else: maximum = amount

	# if amount > 1:
	# 	# get contributions of ech voters
	# 	delay = int(param["--delay"])
	# 	delegate_pubk = delegate.get("publicKey", "")
	# 	accounts = api.Delegate.getVoters(delegate_pubk, returnKey="accounts")
	# 	addresses = [a["address"] for a in accounts] # + hidden
		
	# 	sys.stdout.write("Checking %s-day-true-vote-weight in transaction history...\n" % delay)
	# 	contribution = dict([address, api.getVoteForce(address, days=delay, delegate_pubk=delegate_pubk)] for address in [addr for addr in addresses if addr not in blacklist])
	# 	# apply filters
	# 	C = sum(contribution.values())
	# 	max_C = C*maximum/amount
	# 	# min_C = C*minimum/amount
	# 	cumul = 0
	# 	# first filter
	# 	for address,force in [(a,f) for a,f in contribution.items() if f >= max_C]:
	# 		contribution[address] = max_C
	# 		cumul += force - max_C
	# 	# report cutted share
	# 	untouched_pairs = sorted([(a,f) for a,f in contribution.items() if f < max_C], key=lambda e:e[-1], reverse=True)
	# 	n, i = len(untouched_pairs), 0
	# 	bounty = cumul / max(1, n)
	# 	for address,force in untouched_pairs:
	# 		i += 1
	# 		n -= 1
	# 		if force + bounty > max_C:
	# 			contribution[address] = max_C
	# 			cumul -= abs(C_max - force)
	# 			bounty = cumul / n
	# 		else:
	# 			break
	# 	for address,force in untouched_pairs[i:]:
	# 		contribution[address] += bounty

	# 	# normalize contribution
	# 	k = 1.0/max(1, sum(contribution.values()))
	# 	contribution = dict((a, s*k) for a,s in contribution.items())

	# 	# send payroll
	# 	round_ = loadRound("%s.rnd" % param["<username>"])
	# 	payroll = amount * 100000000.
	# 	minimum *= 100000000.

	# 	transactions = []
	# 	log = collections.OrderedDict()
	# 	log["ADDRESS [WEIGHT]"] = "SHARE"
	# 	for address, weight in sorted(contribution.items(), key=lambda e:e[-1], reverse=True):
	# 		payout = payroll * weight + round_.get(address, 0.) - cfg.fees["send"]
	# 		if payout > minimum:
	# 			transactions.append([payout, address])
	# 			log["%s [%.2f%%]" % (address, weight*100)] = "%s %.8f" % (cfg.token, payout/100000000)
	# 			round_.pop(address, None)
	# 		elif payout != 0:
	# 			round_[address] = payout + cfg.fees["send"]
	# 			log["%s [%.2f%%]" % (address, weight*100)] = "%s %.8f cumuled" % (cfg.token, payout/100000000)

	# 		if len(log):
	# 			prettyPrint(log)
	# 			if askYesOrNo("Validate ?"):
	# 				for (payout, recipientId) in transactions:
	# 					sys.stdout.write("Sending A%.8f to %s...\n" % (payout/100000000, recipientId))
	# 					prettyPrint(api.sendPayload(payout, recipientId, secret, secondSecret))

	# 				prettyPrint(round_)
	# 				if askYesOrNo("Validate cumul ?"):
	# 					dumpRound(round_, "%s.rnd" % param["<username>"])
	# 			else:
	# 				sys.stdout.write("Broadcast canceled\n")

if __name__ == "__main__":
	pass

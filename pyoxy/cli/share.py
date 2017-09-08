# -*- encoding: utf8 -*-
# © Toons

from .. import __PY3__, __FROZEN__, ROOT, api, cfg, util

import os, io, sys, json

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

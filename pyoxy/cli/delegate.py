# -*- encoding: utf8 -*-
# © Toons

'''
Usage: delegate link <secret> [<2ndSecret>]
       delegate unlink
       delegate status
       delegate share <amount> [-c -b <blacklist> -d <delay> -l <lowest> -h <highest>]

Options:
-b <blacklist> --blacklist <blacklist> account addresses to exclude (comma-separated list or pathfile)
-h <highest> --highest <hihgest>       maximum payout during payroll
-l <lowest> --lowest <lowest>          minimum payout during payroll
-d <delay> --delay <delay>             number of fidelity-day [default: 30]
-c --complement                        share the amount complement

Subcommands:
    link     : link to account using secret passphrases. If secret passphrases
               contains spaces, it must be enclosed within double quotes
               ("secret with spaces"). If no secret given, it tries to link
               with saved account(s).
    unlink   : unlink account.
    status   : show information about linked account.
    share    : send ARK amount to address. You can set a 64-char message.
'''

from .. import ROOT, cfg, api, util, crypto

import io, os, sys

ADDRESS = None
PUBLICKEY = None
PRIVKEY1 = None
PRIVKEY2 = None

def link(param):
	global ADDRESS, PUBLICKEY, PRIVKEY1, PRIVKEY2
	
	if param["<secret>"]:
		PUBLICKEY, PRIVKEY1 = crypto.getKeys(param["<secret>"].encode("ascii"))
		if not _checkifdelegate():
			sys.stdout.write("%s is not a valid delegate public key !\n" % PUBLICKEY)
			unlink({})
			return
		ADDRESS = crypto.getAddress(PUBLICKEY)

	account = api.GET.accounts(address=ADDRESS)
	if account["success"]:
		account = account["account"]
		if account["secondSignature"] and param["<2ndSecret>"]:
			PUBKEY2, PRIVKEY2 = crypto.getKeys(param["<2ndSecret>"].encode("ascii"))
			if PUBKEY2 != account["secondPublicKey"]:
				sys.stdout.write("Incorrect second passphrase !\n")
				unlink({})
				return
	else:
		sys.stdout.write("Account does not exist in blockchain\n")
		return

def unlink(param):
	global ADDRESS, PUBLICKEY, PRIVKEY1, PRIVKEY2
	ADDRESS, PUBLICKEY, PRIVKEY1, PRIVKEY2 = None, None, None, None

def status(param):
	if ADDRESS:
		util.prettyPrint(api.GET.delegates.get(publicKey=PUBLICKEY, returnKey="delegate"))
	else:
		sys.stdout.write("No linked account\n")

def share(param):
	pass

# --------------
def _whereami():
	if ADDRESS:
		return "delegate[%s]" % util.shortAddress(ADDRESS)
	else:
		return "delegate"

def _checkifdelegate():
	global DELEGATE

	i = 0
	search = api.GET.delegates(offset=i*201, limit=201, returnKey='delegates')
	while len(search) >= 201:
		i += 1
		if len([d for d in search if d["publicKey"] == PUBLICKEY]): return True
		else: search = api.GET.delegates(offset=i*201, limit=201, returnKey='delegates')

	return False

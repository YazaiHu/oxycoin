Copyright 2017 **Toons**, `MIT licence`_

Install
=======

Ubuntu / OSX
^^^^^^^^^^^^

From development version

``sudo -H pip install git+https://github.com/Moustikitos/oxycoin.git``

If you work with ``python3``

``sudo -H pip3 install git+https://github.com/Moustikitos/oxycoin.git``

Windows 
^^^^^^^

From development version

``pip install git+https://github.com/Moustikitos/oxycoin.git``

Using ``pyoxy``
===============

Use Oxycoin API
^^^^^^^^^^^^^^^

``api`` module allows developpers to send requests to the blockchain. For
security reason only run ``POST`` and ``PUT`` entrypoints from blockchain node.

>>> from pyoxy import api
>>> api.use("toxy") # work on testnet


All entrypoints can be reach using this syntax :

``api.[METHOD].[entrypoint with "/" replaced by "."](param=value, ...[returnKey=name])``

>>> # http equivalent [PEER ADDRESS]/api/delegates/get?username=toons
>>> api.GET.delegates.get(username="toons")
{'delegate': {'address': '12773656026018032534X', 'vote': '50649323252343', 'pub
licKey': '926f731a0fbc04d845fe10f6d4917c47317704af55151c08e07be6616220ddaf', 'us
ername': 'toons', 'rank': 28, 'rate': 28, 'approval': 0.5, 'producedblocks': 154
, 'missedblocks': 0, 'productivity': 100}, 'success': True}

It returns a python dictionary transposed from server json response. You can
provide a ``returnKey`` option value to get the field you want from server response

>>> api.GET.delegates.get(username="toons", returnKey="delegate")
{'address': '12773656026018032534X', 'vote': '50649323252343', 'publicKey': '926
f731a0fbc04d845fe10f6d4917c47317704af55151c08e07be6616220ddaf', 'username': 'too
ns', 'rank': 28, 'rate': 28, 'approval': 0.5, 'producedblocks': 154, 'missedbloc
ks': 0, 'productivity': 100}

Send Oxycoin
^^^^^^^^^^^^

``pyoxy`` bakes transaction localy using ``pynacl`` crypto library so no secret is
sent trough the network. only ``type-0`` transaction can be broadcasted for now.
Amount is given in SATOSHI.

>>> from pyoxy import api, util
>>> api.use("toxy") 
>>> util.sendTransaction(amount=100000000, recipientId="15981732227677853647X", secret="your secret")
{'success': True}

Authors
=======

Toons <moustikitos@gmail.com>

Support this project
====================

+ Toons Bitcoin address: ``1qjHtN5SuzvcA8RZSxNPuf79iyLaVjxfc``
+ Toons Oxycoin address: ``12427608128403844156X``
+ Vote for **toons** delegate on oxycoin blockchain

Version
=======

**0.1**

+ first release

.. _MIT licence: http://htmlpreview.github.com/?https://github.com/Moustikitos/oxycoin/blob/master/pyoxy.html

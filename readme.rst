Copyright 2017 **Toons**, `MIT licence`_

Install
=======

Ubuntu / OSX
^^^^^^^^^^^^

From development version

``sudo -H pip install git+https://github.com/Moustikitos/pyoxy.git``

If you work with ``python3``

``sudo -H pip3 install git+https://github.com/Moustikitos/pyoxy.git``

Windows 
^^^^^^^

From development version

``pip install git+https://github.com/Moustikitos/pyoxy.git``

Using ``pyoxy``
===============

**api module**

``api`` module allows developpers to send requests to the blockchain. For
security reason only run ``POST`` and ``PUT`` entrypoints from blockchain node.

>>> from pyoxy import api
>>> api.use("toxy") # work on testnet
>>> # http equivalent [PEER ADDRESS]/api/delegates/get?username=toons
>>> api.GET.delegates.get(username="toons")
{'delegate': {'address': '12773656026018032534X', 'vote': '50649323252343', 'pub
licKey': '926f731a0fbc04d845fe10f6d4917c47317704af55151c08e07be6616220ddaf', 'us
ername': 'toons', 'rank': 28, 'rate': 28, 'approval': 0.5, 'producedblocks': 154
, 'missedblocks': 0, 'productivity': 100}, 'success': True}

Authors
=======

Toons <moustikitos@gmail.com>

Support this project
====================

.. image:: http://bruno.thoorens.free.fr/img/bitcoin.png
   :width: 100

Toons Bitcoin address: ``1qjHtN5SuzvcA8RZSxNPuf79iyLaVjxfc``

Vote for **toons** delegate on oxycoin blockchain

Version
=======

**0.1**

+ first release

.. _MIT licence: http://htmlpreview.github.com/?https://github.com/Moustikitos/pyoxy/blob/master/pyoxy.html

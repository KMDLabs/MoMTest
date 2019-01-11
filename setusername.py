#!/usr/bin/env python3
# pip3 install python-bitcoinlib

import sys
import kmdrpc
import pprint
import bitcoin
import ast
from conf import CoinParams
from bitcoin.wallet import P2PKHBitcoinAddress
from bitcoin.core import x

CHAIN = sys.argv[1]
USERNAME = sys.argv[2]
PASSWORD = sys.argv[3]
pubkey = kmdrpc.getpubkey_rpc(CHAIN)
bitcoin.params = CoinParams

addr = str(P2PKHBitcoinAddress.from_pubkey(x(pubkey)))
signmessage_result = kmdrpc.signmessage_rpc(CHAIN, addr, USERNAME)
value = signmessage_result + USERNAME

kvupdate_result = kmdrpc.kvupdate_rpc(CHAIN, addr, value, 100, PASSWORD)
pprint.pprint(kvupdate_result)


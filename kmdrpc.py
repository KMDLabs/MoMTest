#!/usr/bin/env python3
import re
import os
import requests
import json
import platform
import sys


# define function that fetchs rpc creds from .conf
def def_credentials(chain):
    operating_system = platform.system()
    if operating_system == 'Darwin':
        ac_dir = os.environ['HOME'] + '/Library/Application Support/Komodo'
    elif operating_system == 'Linux':
        ac_dir = os.environ['HOME'] + '/.komodo'
    elif operating_system == 'Win64':
        ac_dir = "dont have windows machine now to test"
    # define config file path
    if chain == 'KMD':
        coin_config_file = str(ac_dir + '/komodo.conf')
    else:
        coin_config_file = str(ac_dir + '/' + chain + '/' + chain + '.conf')
    # define rpc creds
    with open(coin_config_file, 'r') as f:
        for line in f:
            l = line.rstrip()
            if re.search('rpcuser', l):
                rpcuser = l.replace('rpcuser=', '')
            elif re.search('rpcpassword', l):
                rpcpassword = l.replace('rpcpassword=', '')
            elif re.search('rpcport', l):
                rpcport = l.replace('rpcport=', '')
    return('http://' + rpcuser + ':' + rpcpassword + '@127.0.0.1:' + rpcport)


# define function that posts json data
def post_rpc(url, payload, auth=None):
    try:
        r = requests.post(url, data=json.dumps(payload), auth=auth)
        rpc_result = json.loads(r.text)
        if rpc_result['result'] is None:
            print(str(payload['method']) + ' rpc call failed with ' + str(rpc_result['error']))
            sys.exit(0)
        else:
            return(rpc_result['result'])
    except Exception as e:
        raise Exception("Couldn't connect to " + url + ": ", e)


# VANILLA RPC


def verifymessage_rpc(chain, address, signature, message):
    verifymessage_payload = {
        "jsonrpc": "1.0",
        "id": "python",
        "method": "verifymessage",
        "params": [
            address,
            signature,
            message
        ]
    }
    verifymessage_result = post_rpc(def_credentials(chain), verifymessage_payload)
    return(verifymessage_result)


def kvsearch_rpc(chain, key):
    kvsearch_payload = {
        "jsonrpc": "1.0",
        "id": "python",
        "method": "kvsearch",
        "params": [
            key
        ]
    }
    kvsearch_result = post_rpc(def_credentials(chain), kvsearch_payload)
    return(kvsearch_result)


def getinfo_rpc(chain):
    getinfo_payload = {
        "jsonrpc": "1.0",
        "id": "python",
        "method": "getinfo",
        "params": []}
    return(post_rpc(def_credentials(chain), getinfo_payload))


def getimports_rpc(chain, block):
    getimports_payload = {
        "jsonrpc": "1.0",
        "id": "python",
        "method": "getimports",
        "params": [
            str(block)
        ]
    }
    return(post_rpc(def_credentials(chain), getimports_payload))


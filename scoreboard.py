#!/usr/bin/env python3
import kmdrpc
import pprint

CHAINS = ['CFEKY','CFEKX']
ORCLCHAIN = 'CFEKY'

chain_score = {}
total_score = {}

for chain in CHAINS:
    getinfo_result = kmdrpc.getinfo_rpc(chain)
    block_count = getinfo_result['blocks']
    imports_list = []
    score = {}
    getimports_result = kmdrpc.getimports_rpc(chain, block_count)

    for block in range(block_count):
        getimports_result = kmdrpc.getimports_rpc(chain, block)
        if not getimports_result['imports']:
            continue
        else:
            for i in getimports_result['imports']:
                if i['address'] in score:
                    score[i['address']] += 1
                else:
                    score[i['address']] = 1
    chain_score[chain] = score
        
for chain in chain_score:
    for address in chain_score[chain]:
        if address in total_score:  
            total_score[address] += chain_score[chain][address]
        else:
            total_score[address] = chain_score[chain][address]

name_total = {}

for address in total_score:
    kvsearch_result = kmdrpc.kvsearch_rpc(ORCLCHAIN, address)
    # if username is set via KV show it
    if 'value' in kvsearch_result:
        # check if username is signed properly
        signature = kvsearch_result['value'][:88]
        value = kvsearch_result['value'][88:]
        try:
            verifymessage_result = kmdrpc.verifymessage_rpc(ORCLCHAIN, address, signature, value)
            if verifymessage_result:
                name_total[kvsearch_result['value'][88:]] = total_score[address]
            else:
                cheater = 'CHEAT:' + kvsearch_result['value'][88:]
                name_total[cheater] = total_score[address]
        except:
            troll = 'TROLL:' + kvsearch_result['value']
            name_total[troll] = total_score[address]
    else:
        name_total[address] = total_score[address]

pprint.pprint(name_total)


#!/usr/bin/env python3
import kmdrpc
import pprint
import sys

CHAINS = ['CFEKY','CFEKX']
ORCLCHAIN = 'CFEKY'

initialchain_score = {}
total_score = {}
latest_blocks = {}
name_total = {}

# create dict of latest block for each chain
def getblockcounts(CHAINS):
    for chain in CHAINS:
        latest_blocks[chain] = kmdrpc.getblockcount_rpc(chain)
    return(latest_blocks)

def assign_name(total_score):
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
                    name = kvsearch_result['value'][88:] + ':' + address
                    name_total[name] = total_score[address]
                else:
                    cheater = 'CHEAT:' + address
                    name_total[cheater] = total_score[address]
            except:
                troll = 'TROLL:' + address
                name_total[troll] = total_score[address]
        else:
            name_total[address] = total_score[address]
    return(name_total)


def get_initial_chain_score(chains):
    initial_blocks = getblockcounts(chains)
    print('initial', initial_blocks)
    for chain in CHAINS:
        score = {}

        for block in range(initial_blocks[chain]):
            getimports_result = kmdrpc.getimports_rpc(chain, block)
            if not getimports_result['imports']:
                continue
            else:
                for i in getimports_result['imports']:
                    if i['address'] in score:
                        score[i['address']] += 1
                    else:
                        score[i['address']] = 1
        initialchain_score[chain] = score
    return(initialchain_score)


def update_score(chain, block):
    getimports_result = kmdrpc.getimports_rpc(chain, block)
    if not getimports_result['imports']:
        print('no imports in ' + chain + ' block ' + str(latest_blocks[chain]))
    else:
        imports = getimports_result['imports']
        for imports_dict in imports:
            if imports_dict['address'] in total_score:
                print('CHAIN:' + chain + ' ADDRESS:' + imports_dict['address'] + ' add 1')
                total_score[imports_dict['address']] += 1
            else:
                print('CHAIN:' + chain + ' ADDRESS:' + imports_dict['address'] + ' initialize 1')
                total_score[imports_dict['address']] = 1
    return(total_score)

def chainscore_to_totalscore(chain_score):
    for chain in chain_score:
        for address in chain_score[chain]:
            if address in total_score:
                total_score[address] += chain_score[chain][address]
            else:
                total_score[address] = chain_score[chain][address]
    return(total_score)


initialchain_score = get_initial_chain_score(CHAINS)

total_score = chainscore_to_totalscore(initialchain_score)
name_score = assign_name(total_score)

pprint.pprint(name_score)

latest_printed = {}

chain_score = initialchain_score

lag_blocks = getblockcounts(CHAINS)
print('lag block', lag_blocks)

while True:
    #dummy = input('what:')
    latest_blocks = getblockcounts(CHAINS)
    for chain in latest_blocks:
       try:
           if latest_blocks[chain] != latest_printed[chain]:
                total_score = update_score(chain, latest_blocks[chain])
                print('\nlatest_blocks',latest_blocks)
                pprint.pprint(assign_name(total_score))
                latest_printed[chain] = latest_blocks[chain]
       except:
           latest_printed[chain] = latest_blocks[chain]
        

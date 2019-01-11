# MoMTest
This repo is for the upcoming MoMoM stress tests. 


## Dependencies/Prerequisites :
Follow the instructions in this repo https://github.com/stakedchain/staked to sync the latest CFEK chains. This test will require you to sync at least 2 chains in the same cluster. (same ac_cc value) The tutorial section of this readme assumes you have synced the CFEK chains.

python3, requests and python-bitcoinlib installed 
```shell 
sudo apt-get install python3 python3-pip libssl-dev
pip3 install python-bitcoinlib
pip3 install requests
```

## Tutorial

Clone this repo:
```shell
git clone https://github.com/stakedchain/MoMTest
cd MoMTest
```

The very first thing you should do is set a username for the pubkey you have set in config.ini from the StakedChain/staked repo. It's important that this is a BRAND NEW address. If the address has used previously, it's possible for someone to prevent you from being able to set your username.

```shell
./setusername CFEKY <my_username> <my_password>
```

This will use komodod's Key Value feature to set the key as the associated address and the value as a signed messaged from this address. The signed messaged ensures that the person who has set the key value owns the address.

TODO: add migrate scripts and info on how to use them

The `scoreboard.py` has hard coded chains in it. These will need to be updated prior to the test. The `CHAINS` variable needs to include each chain in the cluster we're competing on. The `ORCLCHAIN` variable needs to be set to the chain we will use for KV usernames. 

The `scoreboard.py` script can be called with no arguments to get the total of all chains on the cluster. It can also be called as `scoreboard.py 1` to show individual scores for each chain. 

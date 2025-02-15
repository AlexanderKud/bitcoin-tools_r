#!/usr/bin/env python3

# sudo apt install python3-pip
# pip3 install hdwallet

# generated is 6 or c, so no Q - bad!

from hdwallet import HDWallet
from hdwallet.symbols import DOGE
from tqdm.contrib.concurrent import process_map
from tqdm import tqdm
import sys, base58

hdwallet = HDWallet(symbol=DOGE)

def pvk_to_wif2(key_hex):
	return base58.b58encode_check(b'\x9e' + bytes.fromhex(key_hex))

def go(k):
	try:
		hdwallet.from_private_key(private_key=k)
	except:
		return
	wif=pvk_to_wif2(k).decode()
	a=wif+'\n'+hdwallet.wif()+'\n'+hdwallet.p2pkh_address()+'\n'+hdwallet.p2sh_address()+'\n\n'
	outfile.write(a)
	outfile.flush()

print('Reading...', flush=True)
infile = open('input.txt','r')
lines = infile.read().splitlines()

print('Writing...', flush=True)
outfile = open('doge.txt','w')
process_map(go, lines, max_workers=16, chunksize=1000)

print('\a',end='',file=sys.stderr)

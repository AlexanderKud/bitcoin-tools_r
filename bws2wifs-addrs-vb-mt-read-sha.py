#!/usr/bin/env python3

from hdwallet import HDWallet
from hdwallet.cryptocurrencies import Bitcoin as BTC
from hdwallet.derivations import IDerivation
from hdwallet.entropies import BIP39Entropy
from hdwallet.hds import BIP32HD, BIP44HD, BIP49HD, BIP84HD, BIP86HD, BIP141HD
from hdwallet.mnemonics import BIP39Mnemonic
from hdwallet.seeds import BIP39Seed
from mnemonic import Mnemonic
from multiprocessing import Pool
from pprint import pprint
from subprocess import check_output
from tqdm import tqdm
from tqdm.contrib.concurrent import process_map
import base58
import concurrent.futures
import hashlib
import math
import os
import pprint
import random
import sys

def pvk_to_wif2(key_hex):
	return base58.b58encode_check(b'\x80' + bytes.fromhex(key_hex)).decode()

infile = open('input.txt','rb')
i=infile.tell()
tmp = 0
cnt = 100

def go(x):
	global tmp, i
	sha=hashlib.sha256(x).digest()
	for x in range(0, 257):
		if x!=0:
			sha=hashlib.sha256(sha).digest()
		try:
			hdwallet1 = HDWallet(cryptocurrency=BTC, hd=BIP32HD).from_private_key(private_key=sha)
		except:
			return
		pvk=hdwallet1.private_key()
		wif1=pvk_to_wif2(pvk)
		w=f'{wif1}\n{hdwallet1.wif()}\n{hdwallet1.address("P2PKH")}\n{hdwallet1.address("P2SH")}\n{hdwallet1.address("P2TR")}\n{hdwallet1.address("P2WPKH")}\n{hdwallet1.address("P2WPKH-In-P2SH")}\n{hdwallet1.address("P2WSH")}\n{hdwallet1.address("P2WSH-In-P2SH")}\n\n'
		outfile.write(w)
		outfile.flush()
	i=infile.tell()
	r=i-tmp
	if r>cnt:
		tmp=i
		pbar.update(r)
		pbar.refresh()

outfile = open('output.txt','w')

size = os.path.getsize('input.txt')
th=16

if __name__=='__main__':
	pbar = tqdm(total=size)
	with Pool(processes=th) as p, tqdm(total=size) as pbar:
		for result in p.imap(go, infile):
			pass

	print('\a', end='', file=sys.stderr)

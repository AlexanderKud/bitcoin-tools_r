#!/usr/bin/env python3

from Crypto.Hash import keccak
from ecpy.curves import Curve
from subprocess import check_output
from tqdm import tqdm
from tqdm.contrib.concurrent import process_map
from web3 import Web3
import base58
import hashlib
import os

alchemy_url = "https://eth-mainnet.g.alchemy.com/v2/YOUR_API_KEY"
w3 = Web3(Web3.HTTPProvider(alchemy_url))

outfile = open("eth-range.txt","a")

cnt=2000000

def bytes_to_int(bytes):
	return int.from_bytes(bytes,"big")

def go(x):
	private_key=bytes_to_int(os.urandom(32))
	cv	 = Curve.get_curve('secp256k1')
	pu_key = private_key * cv.generator # just multiplying the private key by generator point (EC multiplication)
	concat_x_y = pu_key.x.to_bytes(32, byteorder='big') + pu_key.y.to_bytes(32, byteorder='big')
	k=keccak.new(digest_bits=256)
	eth_addr = '0x' + k.update(concat_x_y).digest()[-20:].hex()
	bal=w3.eth.get_balance(w3.to_checksum_address(eth_addr),"latest")
	if bal>0:
		print("Found one!\a")
	outfile.write(hex(private_key)+" "+eth_addr+" "+str(bal)+"\n")
	outfile.flush()
	return

process_map(go, range(1,cnt+1), max_workers=4, chunksize=1000)

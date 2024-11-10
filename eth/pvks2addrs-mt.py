#!/usr/bin/env python3

from Crypto.Hash import keccak
from ecpy.curves import Curve
from tqdm import tqdm
import hashlib
from web3 import Web3
from tqdm.contrib.concurrent import process_map

i=open('input.txt','r')
o=open('output.txt','w')

def go(l):
	l=l.strip()
	private_key = int(l,16)

	cv     = Curve.get_curve('secp256k1')
	pu_key = private_key * cv.generator # just multiplying the private key by generator point (EC multiplication)

	concat_x_y = pu_key.x.to_bytes(32, byteorder='big') + pu_key.y.to_bytes(32, byteorder='big')
	k=keccak.new(digest_bits=256)
	k.update(concat_x_y)
	eth_addr = '0x' + k.hexdigest()[-40:]

	cksum=Web3.to_checksum_address(eth_addr)
	o.write(l+' : '+cksum+'\n')
	o.flush()

process_map(go, i, max_workers=4, chunksize=4000)

o.close()

#!/usr/bin/env python3

import base58
import binascii
import ecdsa
import ecdsa.der
import ecdsa.util
import hashlib
import math
import random
import re
import struct
import unittest
# import utils
from ecdsa import SigningKey, SECP256k1

def b58_to_bytes(s):
	return base58.b58decode_check(s)

def bytes_to_b58(bytes):
	return base58.b58encode_check(bytes)

def bytes_to_str(bytes):
	return bytes.decode("utf-8")

def bytes_to_int(bytes):
	result = 0
	for b in bytes:
		result = result * 256 + int(b)
	return result

def bytes_to_int2(bytes):
	return int.from_bytes(bytes,"big")

def bytes_to_hex(bytes):
	return bytes.hex()

def count_lines(file):
	return sum(1 for line in open(file, 'r'))

def hex_to_bytes(hex):
	return bytes.fromhex(hex)

def hex_to_int(hex):
	return int(hex, 16)

#def int_to_bytes(i):
#	return chr(i).encode()

#def int_to_bytes2(i):
#	return bytearray([i])

def int_to_bytes3(value, length = None):
	if not length and value == 0:
		result = [0]
	else:
		result = []
		for i in range(0, length or 1+int(math.log(value, 2**8))):
			result.append(value >> (i * 8) & 0xff)
		result.reverse()
	return str(bytearray(result))

def int_to_bytes4(number, length):
	# length = zero-fill bytes
	return number.to_bytes(length,'big')

#def int_to_bytes5(number):
#	return str.encode(str(number))

def int_to_str(number):
	return str(number)

def int_to_hex(i):
	return hex(i)

def pubkey_to_addr(pk):
	if (ord(bytearray.fromhex(pk[-2:])) % 2 == 0):
		public_key_compressed = '02'
	else:
		public_key_compressed = '03'
	public_key_compressed += pk[2:66]
	hex_str = bytearray.fromhex(public_key_compressed)
	sha = hashlib.sha256()
	sha.update(hex_str)
	rip = hashlib.new('ripemd160')
	rip.update(sha.digest())
	key_hash = rip.hexdigest()
	modified_key_hash = "00" + key_hash
	sha = hashlib.sha256()
	hex_str = bytearray.fromhex(modified_key_hash)
	sha.update(hex_str)
	sha_2 = hashlib.sha256()
	sha_2.update(sha.digest())
	checksum = sha_2.hexdigest()[:8]
	byte_25_address = modified_key_hash + checksum
	return base58.b58encode(bytes(bytearray.fromhex(byte_25_address))).decode('utf-8')

def pvk_to_addr(s):
	return pubkey_to_addr(pvk_to_pubkey(s))

def pvk_to_wif(key_bytes):
	return base58.b58encode_check(b'\x80' + key_bytes)

def pvk_to_wif2(key_hex):
	return base58.b58encode_check(b'\x80' + bytes.fromhex(key_hex))

def pvk_to_pubkey(h):
	sk = ecdsa.SigningKey.from_string(h, curve=ecdsa.SECP256k1)
	vk = sk.verifying_key
	return (b'\04' + sk.verifying_key.to_string()).hex()

def reverse_string(s):
	return s[::-1]

def str_to_bytes(text):
	return str.encode(text)

def str_to_hex(text):
	#return "".join(hex(chr(int(x,8))) for x in text)
	return binascii.hexlify(text.encode()).decode()

def wif_to_pvk(s):
	return base58.b58decode_check(s).hex()

print(b58_to_bytes("1KFHE7w8BhaENAswwryaoccDb6qcT6DbYY"))
print(bytes_to_b58(b'\x00\xc8%\xa1\xec\xf2\xa6\x83\x0cD\x01b\x0c:\x16\xf1\x99PW\xc2\xab'))
print(bytes_to_str(b'abc123'))
print(bytes_to_int(b'\x80\x00'))
print(bytes_to_int2(b'\x80\x00'))
print(bytes_to_hex(b'\x80\x00'))
print(count_lines('_snippets.py'))
print(hex_to_bytes('8000'))
print(hex_to_int('8000'))
print(int_to_bytes3(32768))
print(int_to_str(65))
print(int_to_hex(32768))
print(pubkey_to_addr('0430210c23b1a047bc9bdbb13448e67deddc108946de6de639bcc75d47c0216b1be383c4a8ed4fac77c0d2ad737d8499a362f483f8fe39d1e86aaed578a9455dfc'))
print(pvk_to_addr(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\xA8\x38\xB1\x35\x05\xB2\x68\x67'))
print(pvk_to_wif(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\xA8\x38\xB1\x35\x05\xB2\x68\x67'))
print(pvk_to_wif2('000000000000000000000000000000000000000000000001a838b13505b26867'))
print(pvk_to_pubkey(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\xA8\x38\xB1\x35\x05\xB2\x68\x67'))
print(reverse_string('abc def xyz'))
print(str_to_bytes('ABC'))
print(str_to_hex('ABC'))
print(wif_to_pvk('5HpHagT65TZzG1PH3CSu63k8DbpvD8s5ipCnYRNeQuRFKarWVVs'))

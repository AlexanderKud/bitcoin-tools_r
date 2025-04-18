#!/usr/bin/env python3

import random
from tqdm import tqdm

i=1

def go(i, x):
	random.seed(a=x, version=1)

	while i<=2**160:
		l=i
		h=i*2
		print(hex(random.randrange(l,h)), end=' ')
		i=i*2

	print()

for j in tqdm(range(0,1000001)):
	go(i, j)

#!/usr/bin/env python3

from pprint import pprint

result = []
delim=','
rows=0

for line in open("input_file.csv"):
	line=line.strip()
	row=line.split(delim)
	newrow=[]
	for r in row:
		newrow.append(int(r))
	result.append(newrow)
	rows=rows+1

cols=len(row)

pprint(result)
print('rows: '+str(rows))
print('cols: '+str(cols))

# you get array of rows consisting of array of columns, all text

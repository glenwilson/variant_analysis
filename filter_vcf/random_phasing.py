#!/usr/bin/python 

import sys 
import csv
import random

inputlist= sys.argv
inputlist.pop(0)

for filename in inputlist: 
	f = open(filename, 'r')
	g = open(filename[:-4]+"-rand.vcf", 'w')
	reader = csv.reader(f, delimiter='\t', quotechar=None, doublequote=False)
	writer = csv.writer(g, delimiter='\t', quotechar=None)
	for row in reader:
		if row[0][0] == "#":
			writer.writerow(row)
		else:
                        newrow = row[:]
                        if random.randint(0,1):
                                newrow[9] = newrow[9][0] + '|' + newrow[9][2]
                        else:
                                newrow[9] = newrow[9][2] + '|' + newrow[9][0]
                        writer.writerow(newrow)
	g.close()
	f.close()

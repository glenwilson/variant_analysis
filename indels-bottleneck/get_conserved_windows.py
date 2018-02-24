#!/usr/bin/python

import csv
import sys

#load the variant vcf files
inputlist = sys.argv[1:]

#this opens csv of windows
win = open('nblrr-noscaffold-windows.csv', 'r')
wincsv = csv.reader(win, delimiter='\t', quotechar=None, doublequote=False)
winlist = [row for row in wincsv]

#file to write conserved regions to
out = open('conserved_regions-nblrr.csv', 'w')
outcsv = csv.writer(out, delimiter='\t', quotechar=None, doublequote=False)

#number of windows to extract 
#look to left and right of window by offset base pairs for conserved regions
offset = 50

def make_list(a, start, stop, n=20):
	"""a is a list of pairs of integers, (x, len) with x the start of a
        closed interval, and len the length of the interval, so closed
        interval is [x, x+len-1]. 

        We union up the intervals determined by a and return the complement 
        [start, stop] - union(a) in terms of intervals. We describe intervals
        as (x, len) again. 

        a is assumed to be in increasing order on the x coordinate. 

	output is a list of tuples which describe intervals in [start, stop]
	which don't contain the elements of a, given in form (x, len)

        ? Is output (start, stop) or (x, len)? it is (x, len) with x the start. 
        """
	out = []
	x = start
	b = a[:]
	while b:
		y = b.pop(0)
		if y[0]-x >= n:
			out.append((x, y[0]-x))
		x = max(x, y[0] + y[1])			
	if stop + 1 - x >= n:
		out.append((x, stop-x+1))
	return out

#################################################################

for row in winlist[1:]:
        chrom = int(row[0][-2:])
	start = int(row[2]) 
	stop = int(row[3]) 
	var_pos = []
	for name in inputlist:
		vcf = open(name, 'r')
		vcfcsv = csv.reader(vcf, delimiter='\t', quotechar=None, doublequote=False)
		for en in [x for x in vcfcsv if len(x)>2 and x[0][0] != "#" and int(x[0][-2:]) == chrom and start-50 <= int(x[1]) <= stop+50]:
                        a = en[4].split(",")
			length = max(1, len(en[3]) - len(a[0]) + 1)
			if len(a) == 2 :
				length = max(length, len(en[3]) - len(a[1]) + 1)
                        var_pos.append((int(en[1]), length))
                vcf.close()
        var_pos = sorted(var_pos, key=lambda pair: pair[0])
	newrow = row[:4]
	newrow.extend(make_list(var_pos, start-50, stop+50))
	outcsv.writerow(newrow)

#!/usr/bin/python

import csv

#this opens csv of conserved regions
reg = open('conserved_regions-nblrr.csv', 'r')
regcsv = csv.reader(reg, delimiter='\t', quotechar=None, doublequote=False)

out = open('primer3-windows.csv', 'w')
outcsv = csv.writer(out, delimiter='\t', quotechar=None, doublequote=False)

#look to left and right of window by offset base pairs for conserved regions
offset = 50

outcsv.writerow(["chromosome", "name", "start", "stop", "length", "primer location quadruplets"])

for row in regcsv:
        entries = row[4:]
        for i in range(len(entries)):
                for j in range(i+1, len(entries)):
                        newrow = row[:2]
                        a = entries[i][1:-1]
                        a = a.split(',')
                        a = [int(x) for x in a]
                        b = entries[j][1:-1]
                        b = b.split(',')
                        b = [int(x) for x in b]
                        if 1200 >= b[0] + b[1] - a[0] >= 200:
                                newrow.extend([a[0], b[0] + b[1] - 1 , b[0]+b[1]-a[0], str(a[0])+","+str(a[1])+","+str(b[0])+","+str(b[1])])
                                outcsv.writerow(newrow)

reg.close()
out.close()
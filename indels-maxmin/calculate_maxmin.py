#!/usr/bin/python

#this program calculates the difference in lengths of
#regions given in each row of csv file for all variants
#given at command line

import sys 
import csv
import re

inputlist= sys.argv
inputlist.pop(0)

#Open file with windows, 
win = open('windows_with_primers.csv', 'r')
wincsv = csv.reader(win, delimiter='\t', quotechar=None)

#Open file to write
out = open('wins_primers-maxmin-np.csv', 'w')
outcsv = csv.writer(out, delimiter='\t', quotechar=None)
header = wincsv.next()
outlist = [row for row in wincsv]

#this initializes each column for a variant with all zeros
for row in outlist:
    row.extend([0 for i in 2*range(len(inputlist))])

#q+5 is the column for the qth variant in the inputlist
for q in range(len(inputlist)):
    f = open(inputlist[q], 'r')
    fcsv = csv.reader(f, delimiter='\t', quotechar=None, doublequote=False)
    for entry in fcsv:
        if len(entry) < 2 and entry[0][0] != "#":
            pass
        else:
           for row in [x for x in outlist if (x[0] == entry[0] and
                                              int(x[2]) <=
                                              int(entry[1]) <=
                                              int(x[3]))]:
                a = entry[4].split(",")
                #if both homologs have variant, add to max and min col
                if entry[9][0] =="1" and entry[9][2] =="1":
                    row[2*q + 6] += len(a[0]) -len(entry[3])
                    row[2*q + 7] += len(a[0]) -len(entry[3])
                #if only one homolog has variant, add to first col if
                #a deletion, add to second col if insertion
                if entry[9][0] == "0" or entry[9][2] == "0":
                    if len(a[0]) - len(entry[3]) < 0:
                        row[2*q + 6] += len(a[0]) - len(entry[3])
                    else:
                        row[2*q + 7] += len(a[0]) - len(entry[3])
                #if there are two variant for this position, then
                #add the difference appropriately to the right columns
                if entry[9][0] == "2" or entry[9][2] == "2":
                    row[2*q+6] += min(len(a[1]) - len(entry[3]), len(a[0]) - len(entry[3]))
                    row[2*q+7] += max(len(a[1]) - len(entry[3]), len(a[0]) - len(entry[3]))
    f.close()
    
#this makes a header to indicate what the columns mean
header = ["chromosome", "nblrr", "start", "stop", "9509 length", 'penalty']
for filename in inputlist:
    m = re.search('[0-9][0-9][0-9][0-9]', filename)
    header.append(m.group(0) + "homolog 1")
    header.append(m.group(0) + "homolog 2")
outlist.insert(0, header)
#this writes the constructed list of rows to the csv file
for row in outlist:
    outcsv.writerow(row)
out.close()
        


    
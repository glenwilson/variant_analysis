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
out = open('windows_with_primers-snps.csv', 'w')
outcsv = csv.writer(out, delimiter='\t', quotechar=None)
header = wincsv.next()
outlist = [row for row in wincsv]

#this initializes each column for a variant with all zeros
N = len(inputlist)
for row in outlist:
    row.extend([0 for i in range(N+ N*(N-1)/2)])

#record the NUMBER of indels in each window of each variant

def is_snp(row):
    if not ',' in row[4]:
        if len(row[3]) == len(row[4]):
            return True
    else:
        x = row[4].split(',')
        if len(row[3]) == len(x[0]) and len(row[3]) == len(x[1]):
            return True
    return False

for q in range(len(inputlist)):
    f = open(inputlist[q], 'r')
    fcsv = csv.reader(f, delimiter='\t', quotechar=None,
                      doublequote=False)
    for entry in fcsv:
        if len(entry) < 2 and entry[0][0] != "#":
            pass
        else:
            for row in [x for x in outlist if (x[0] == entry[0] and
                                               int(x[2]) <=
                                               int(entry[1]) <=
                                               int(x[3]))]:
                if not is_snp(entry):
                    row[q+6] += 1
    f.close()
                       
    #double check index! I add 1 before the first time index is used.
index = N + 5
for q in range(N):
    f = open(inputlist[q], 'r')
    fcsv = csv.reader(f, delimiter='\t', quotechar=None,
                      doublequote=False)
    flist = [row for row in fcsv]
    for r in range(q+1, N):
        g = open(inputlist[r], 'r')
        gcsv = csv.reader(g, delimiter='\t', quotechar=None,
                          doublequote=False)
        glist = [row for row in gcsv]
        index += 1
        for row in outlist:
            print row[1] + " " + str(index)
            list1 = [x for x in flist[:] if (x[0] == row[0] and
                                         int(row[2]) <= int(x[1])
                                         <= int(row[3]))]
            list2 = [x for x in glist[:] if (x[0] == row[0] and
                                         int(row[2]) <= int(x[1])
                                         <= int(row[3]))]
            dict1 = {}
            dict2 = {}
            for x in list1:
                dict1[x[1]] = x
            for x in list2:
                dict2[x[1]] = x
            keys1 = dict1.keys()[:]
            for pos in keys1:
                if is_snp(dict1[pos]):
                    try:
                        if is_snp(dict2[pos]):
                            a = set(dict1[pos][4].split(','))
                            b = set(dict2[pos][4].split(','))
                            if a != b:
                                row[index] += 1
                        del dict2[pos]
                    except KeyError:
                        row[index] += 1
                else:
                    del dict1[pos]
            for pos in dict2:
                if is_snp(dict2[pos]):
                    try:
                        if is_snp(dict1[pos]):
                            a = set(dict1[pos][4].split(','))
                            b = set(dict2[pos][4].split(','))
                            if a != b:
                                row[index] += 1
                    except KeyError:
                        row[index] += 1
        g.close()
    f.close()
    
#this makes a header to indicate what the columns mean
header = ["chromosome", "nblrr", "start", "stop", "9509 length", 'penalty']
for filename in inputlist:
    m = re.search('[0-9][0-9][0-9][0-9]', filename)
    header.append(m.group(0) + "indels")
for q in range(N):
    for r in range(q+1,N):
        m1 = re.search('[0-9][0-9][0-9][0-9]', inputlist[q])
        m2 = re.search('[0-9][0-9][0-9][0-9]', inputlist[r])
        header.append("[" + m1.group(0) +", " + m2.group(0) + "]")
outlist.insert(0, header)
#this writes the constructed list of rows to the csv file
for row in outlist:
    outcsv.writerow(row)
out.close()

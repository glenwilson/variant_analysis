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
win = open('windows.csv', 'r')
wincsv = csv.reader(win, delimiter='\t', quotechar=None)
header = wincsv.next()

for row in wincsv:
    #Open file to write
    out = open('Qusl-Simple' + row[1] + '-' + row[2] + '-' + row[3] + '.csv', 'w')
    outcsv = csv.writer(out, delimiter='\t', quotechar=None)
    #go through vcf files, write rows to output
    print row[0]
    print row[1]
    print row[2]
    print row[3]
    for q in range(len(inputlist)):
        f = open(inputlist[q], 'r')
        fcsv = csv.reader(f, delimiter='\t', quotechar=None, doublequote=False)
        m = re.search('[0-9][0-9][0-9][0-9]', inputlist[q])
        outcsv.writerow([])
        outcsv.writerow([m.group(0)])
        for entry in fcsv:
            if entry[0][0] != "#" and int(row[2]) <= int(entry[1]) <= int(row[3]) and entry[0] == row[0]:
                outcsv.writerow(entry)
        f.close()
    out.close()
win.close()

        


    

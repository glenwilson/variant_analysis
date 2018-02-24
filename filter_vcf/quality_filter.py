#!/usr/bin/python

import sys
import csv

#command line arguments the vcf files to be filtered
inputlist= sys.argv
inputlist.pop(0)

suffix = 'qual.vcf'
quality = 800

for filename in inputlist:
    vcf = open(filename, 'r')
    vcfcsv = csv.reader(vcf, delimiter='\t', quotechar=None, doublequote=False)
    out = open(filename[:-4]+suffix, 'w')
    outcsv = csv.writer(out, delimiter='\t', quotechar=None, doublequote=False)
    for entry in vcfcsv:
        if len(entry) < 2 or entry[0][0] == "#":
            outcsv.writerow(entry)
        elif float(entry[5]) >= quality:
            outcsv.writerow(entry)
    vcf.close()
out.close()


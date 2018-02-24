#!/usr/bin/python 
###################################################################
#This script takes a VCF file given at the command line which lists
#INDELS and SNP variants in the last two columns and combines them
#into a single column.  This is the format that the Spolyrhiza VCF
#files came in.
#
#Simply run as ./make_one_var_col.py My_VCF_File.vcf
#
#The output will have the same file name, but end in onecol.
##################################################################

import sys 
import csv

inputlist= sys.argv
inputlist.pop(0)

for filename in inputlist: 
	f = open(filename, 'r')
	reader = csv.reader(f, delimiter='\t', quotechar=None, doublequote=False)
        out = open(filename[:-4] + "onecol.vcf", 'w')
        outcsv = csv.writer(out, delimiter='\t', quotechar=None)
        for row in reader:
                if row[0][0] == "#":
                        outcsv.writerow(row)
                        continue
                if row[9] == "./.":
                        row.pop(9)
                elif row[10] == "./.":
                        row.pop(10)
                outcsv.writerow(row)
        f.close()
        out.close()

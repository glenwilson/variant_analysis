import csv
import re 

#open the primer3 output
primer3 = open('primer3-files.out', 'r')
primer3f = primer3.read()
primer3l = primer3f.split('=\n')


#this opens csv to write to
win = open('windows_with_primers.csv', 'w')
wincsv = csv.writer(win, delimiter='\t', quotechar=None, doublequote=False)

header = ['chromosome', 'name', 'start', 'stop', 'length', 'penalty']
wincsv.writerow(header)

for entry in primer3l:
    if 'PRIMER_LEFT_0_SEQUENCE=' in entry:
        m =re.search('PRIMER_PAIR_0_PENALTY=[0-9]....', entry)
        penalty = m.group(0)[-5:]
        row = []
        x = entry[:entry.index('\n')]
        x = x[12:]
        y = x.split('-')
        chrom = y[0][2:4]
        row.append('Spolyrhiza9509_20150416_chr'+chrom)
        row.extend([y[0], y[1], y[2], int(y[2])-int(y[1])+1, penalty])
        wincsv.writerow(row)

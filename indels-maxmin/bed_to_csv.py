import csv


#Open bed file as csv object with nblrr names and locations
nblrr = open('Sp9509v3.5_nblrr-noscaffold.bed', 'r')
nblrrcsv = csv.reader(nblrr, delimiter='\t', quotechar=None, doublequote=False)
#Make list of the rows to work with
nblrrlist = []
for row in nblrrcsv:
    nblrrlist.append(row[0:4])
nblrr.close()

#file to write conserved regions to
out = open('nblrr-noscaffold-windows.csv', 'w')
outcsv = csv.writer(out, delimiter='\t', quotechar=None, doublequote=False)

outcsv.writerow(['Chromosome', 'Gene', 'Start', 'Stop'])

for n in nblrrlist:
    start = int(n[1])
    stop = int(n[2])
    chrom = n[0]
    name = n[3][3:13]
    outcsv.writerow([chrom, name, start, stop])

out.close()

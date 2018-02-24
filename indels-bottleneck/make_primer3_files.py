import csv

#this opens csv of windows and conserved regions
win = open('primer3-windows.csv', 'r')
wincsv = csv.reader(win, delimiter='\t', quotechar=None, doublequote=False)

#look to left and right of window by offset base pairs for conserved regions
offset = 50

#This has reference sequence data
f= open('../../Spolyrhiza9509v3.5/Spolyrhiza9509_20150416.fasta', 'r')
a = f.read()
f.close()

#x is a list of chromosome sequences, with some header and newline chars
x = a.split('>')
#this preprocesses entries of x to just be sequences
y = []

#this gets the scaffolds wrong!!! 
for seq in x:
    seq = seq[30:]
    seq = seq.replace('\n', '')  
    y.append(seq)
#x is now a list of chromosome sequences only. 
x=y 

header = wincsv.next()
filename = "primer3-files.txt"
out = open(filename, 'w')
for row in wincsv:
    chrom = int(row[0][-2:])
    start = int(row[2]) 
    stop = int(row[3])
    #the start and stop are given in coordinates of sequence data, which starts the labeling of base pairs at 1 rather than 0.
    seq = x[chrom][start-1:stop]
    quad = row[5].split(',')
    quad = [int(b) for b in quad]
    newquad = [quad[0]-start, quad[1], quad[2]-start, quad[3]]
    newquad = [str(b) for b in newquad]
    newstr = newquad[0]+","+newquad[1]+","+newquad[2]+","+newquad[3]
    out.write("SEQUENCE_ID=" + row[1] + "-" + row[2] + "-" + row[3] + "\n")
    out.write("SEQUENCE_TEMPLATE=" + seq + "\n")
    out.write("PRIMER_THERMODYNAMIC_PARAMETERS_PATH=/home/glen/bin/primer3_config/\n")
    out.write("PRIMER_PRODUCT_SIZE_RANGE=100-1200\n")
    out.write("SEQUENCE_PRIMER_PAIR_OK_REGION_LIST=" + newstr +"\n")
    out.write("PRIMER_MAX_NS_ACCEPTED=1\n")
    out.write("PRIMER_LIBERAL_BASE=1\n")
    out.write("=\n")
out.close()



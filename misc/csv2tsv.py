import csv
import sys
if len(sys.argv) < 3:
    sys.exit("Usage: csv2tsv.py inputfile.csv outputfile.tsv")

outfile=file(sys.argv[2],'w+')
infile=open(sys.argv[1])
freader=csv.reader(infile)
freader.next()
csv.writer(outfile, delimiter="\t").writerows(freader)

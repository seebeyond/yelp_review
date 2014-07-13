# GENERATE SEED DATA FOR PARSER
#
# takes data csv file and extracts review text,
# removes special characters, writes to a txt file
# which can fed to parser for generating sentence parses
#
#
import sys
import json
import re
import csv
import random

#check args
if len(sys.argv) < 5:
	#print str(sys.argv[2])
	print "Args Missing!! \nUsage: generate_parser_seed_data.py <processed.csv> <parser_input.txt> <USEFUL/NOT USEFUL> <SIZE>"
	exit()

#input file
f=open(str(sys.argv[1]))
freader=csv.reader(f)

#output file
outfile=open(str(sys.argv[2]),'w')


#mode
isuseful=int(sys.argv[3]) #0-NOT USEFUL, 1-USEFUL

#size
sz=int(sys.argv[4])

#content=f.readlines()
headers=freader.next()
data = list(freader)


count=0;
random.shuffle(data)

if isuseful==0:
	for row in data:
		if int(row[18])==0:
			content=row[6]
			content=content.replace('\r\n','')
			content=content.replace('\r','')
			content=content.replace('\n','')
			content=content.replace('\t','')
			content=content.replace('(','')
			content=content.replace(')','')
			content=content.replace('[','')
			content=content.replace(']','')
			content=content.replace('{','')
			content=content.replace('}','')
			content=content.replace('..','')
			content=content.replace('...','')
			outfile.write("%s\n" %content);
			count=count+1
			if count == sz:
				break
elif isuseful==1:
        for row in data:
                if int(row[18])>5:
                        content=row[6]
                        content=content.replace('\r\n','')
                        content=content.replace('\r','')
                        content=content.replace('\n','')
                        content=content.replace('\t','')
                        content=content.replace('(','')
                        content=content.replace(')','')
                        content=content.replace('[','')
                        content=content.replace(']','')
                        content=content.replace('{','')
                        content=content.replace('}','')
			content=content.replace('.....','. ')
			content=content.replace('....','. ')
                        content=content.replace('...','. ')
			content=content.replace('..','. ')
			content=content.replace('.','. ')
                        outfile.write("%s\n" %content);
			count=count+1
			if count == sz:
				break

outfile.close()
f.close()

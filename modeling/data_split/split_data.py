#
#
# Generates two CSV files: training-data.csv, testing-data.csv
#
import random
import sys

#check args
if len(sys.argv) < 2:
	#print str(sys.argv[1])
	print "Args Missing!! \nUsage: split_data.py <input_file.csv>"
	exit()

f=open(str(sys.argv[1]))
data=f.read().split('\r\n')

header=data[0]
xdata=data[1:len(data)]
random.shuffle(xdata)

trainingLimit=len(xdata)*90/100
testingLimit=len(xdata)-trainingLimit

trainingsplit=xdata[0:trainingLimit]
testingsplit=xdata[trainingLimit+1:len(xdata)]

trainout=open('training-data.csv','w')
testout=open('testing-data.csv','w')

trainout.write("%s\n" % header)
testout.write("%s\n" % header)

for i in xrange(0,len(trainingsplit)):
	trainout.write("%s\n" % trainingsplit[i])

for i in xrange(0,len(testingsplit)):
	testout.write("%s\n" % testingsplit[i])

trainout.close()
testout.close()
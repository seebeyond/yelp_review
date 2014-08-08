import sys
import csv
import random
#
# from the input training data
# undersample not useful reviews 
# to create balanced classes for 
# model training

# USAGE
# python undersample_notusefulreviews.py <input_training_data.csv> <threshold value> <output_training_data.csv>
#

#check args
if len(sys.argv) < 4:
        #print str(sys.argv[1])
        print "Args Missing!! \nUsage: undersample_notusefulreviews.py <input_training_data.csv> <threshold value> <output_training_data.csv>"
        exit()

infile=open(str(sys.argv[1]))
reader=csv.reader(infile)

outfile=open(str(sys.argv[3]),'w')
writer=csv.writer(outfile)

threshold=int(sys.argv[2])
#skip header
header=reader.next()

usefulReviewInstances=list()
notusefulReviewInstances=list()

#accumulate all not useful review training instances and useful review training instances
for row in reader:
	#print row[18], int(row[18])
	if len(row)==0:
		continue
	if int(row[len(row)-1])<threshold:
		notusefulReviewInstances.append(row)
	elif int(row[len(row)-1])>=threshold:
		usefulReviewInstances.append(row)
	else:
		print "Invalid target for train instance -- CHECK ASAP",row[18]

usefulClassSize=len(usefulReviewInstances)
notusefulClassSize=len(notusefulReviewInstances)

sampleIndices=random.sample(range(notusefulClassSize),usefulClassSize)

newTrainData=list()
for index in sampleIndices:
	newTrainData.append(notusefulReviewInstances[index]);

for record in usefulReviewInstances:
	newTrainData.append(record);

random.shuffle(newTrainData)

writer.writerow(header)
writer.writerows(newTrainData)
outfile.close()
infile.close()
	
	
print "Number of useful review instances : ",usefulClassSize
print "Number of not useful review instances: ", len(sampleIndices)
print "Number of instances in new train data: ", len(newTrainData)

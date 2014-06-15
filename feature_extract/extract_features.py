import sys
import csv

#check args
if len(sys.argv) < 3:
	#print str(sys.argv[1])
	print "Args Missing!! \nUsage: extract_features.py <input_file.csv> <output_file.csv>"
	exit()
infile=open(str(sys.argv[1]))
reader=csv.reader(infile)

def convertType(h,v):
	if h == 'avgstars':
		return float(v)
	elif h == 'yelp_startdate' or h == 'review_date':
		return v
	elif h == 'name' or h == 'id' or h == 'review_id' or h == 'text' or h == 'username':
		return v
	else:
		return int(v)



##
#
# code to read csv file and do proper type mapping for fields
##
headers=reader.next()
data={}
for h in headers:
	data[h]=[]

rowid = 1
for row in reader:
	print rowid
	for h, v in zip(headers, row):
		data[h].append(convertType(h,v))
	rowid=rowid+1

##
# add new length of review text feature
# use this as basis to generate any new feature
# and add to existing data
##

reviewLen=list()

for i in xrange(0,len(data['text'])):
	reviewLen.append(len(data['text'][i]))

#adding new feature as a new key value pair to existing data
data['review_len']=reviewLen


#
# write out updated output.csv
#
#
outfile=open(str(sys.argv[2]),'w')
writer=csv.writer(outfile)
writer.writerow(('id','name','review_count','review_id','review_date','stars','text','review_len','username','avgstars','user_cool','user_funny','user_useful','fans','friendcount','user_reviewcount','yelp_startdate','review_cool','review_funny','review_useful') )


for i in xrange(0,len(data['name'])):
	writer.writerow( (data['id'][i],data['name'][i],data['review_count'][i],data['review_id'][i],data['review_date'][i],data['stars'][i],data['text'][i],data['review_len'][i],data['username'][i],data['avgstars'][i],data['user_cool'][i],data['user_funny'][i],data['user_useful'][i],data['fans'][i],data['friendcount'][i],data['user_reviewcount'][i],data['yelp_startdate'][i],data['review_cool'][i],data['review_funny'][i],data['review_useful'][i]) )

## FEATURE SET 1 (11 FEATURES)
#
# 'review_id' (key),'review_rating','review_len','review_numwords',
# 'review_numsentences','review_avgnumwords','review_age','user_avgstars',
# 'user_usefulcount','user_fancount','user_friendscount','user_reviewcount',
# 'user_yelpexp','review_usefulcount','review_isuseful'
#
#
##

import sys
import csv
import datetime
from datetime import date

#check args
if len(sys.argv) < 3:
	#print str(sys.argv[1])
	print "Args Missing!! \nUsage: extract_featureset1.py <input_file.csv> <output_file.csv>"
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


features=dict()

##
#
# code to read csv file and do proper type mapping for fields
##
headers=reader.next()
data={}
for h in headers:
	data[h]=[]

#rowid = 1
for row in reader:
	#print rowid
	for h, v in zip(headers, row):
		data[h].append(convertType(h,v))
	#rowid=rowid+1

#adding review id, star rating features
features['review_id'] = data['review_id']
features['review_rating'] = data['stars']

##
# add new length of review text feature
# use this as basis to generate any new feature
# and add to existing data
##

reviewLen=list()

for i in xrange(0,len(data['text'])):
	reviewLen.append(len(data['text'][i]))

#adding new feature as a new key value pair to existing data
features['review_len']=reviewLen


#
# add number of words in review as feature from review text
#
numWords=list()

for i in xrange(0,len(data['text'])):
	twords=data['text'][i].split(' ')
	numWords.append(len(twords))

features['review_numwords'] = numWords

#
# add number of sentences, number of words per sentence as feature from review text
#
numSentences=list()
avgNumWords=list()

for i in xrange(0,len(data['text'])):
	sr=data['text'][i]
	rsentences=sr.split('.')
	filtered_sentences=filter(len,rsentences)
	numSentences.append(len(filtered_sentences))
	sumWords=0
	for j in filtered_sentences:
		swords=j.split(' ')
		fswords=filter(len,swords)
		sumWords=sumWords+len(fswords)
	avgNumWords.append(sumWords/len(filtered_sentences))

features['review_numsentences'] = numSentences
features['review_avgnumwords'] = avgNumWords

#
# add review_age as feature from review date
#
review_age=list()
td=date.today()
for i in xrange(0,len(data['review_date'])):
	yd=datetime.datetime.strptime(data['review_date'][i], '%Y-%m-%d').date()
	review_age.append((td-yd).days)

features['review_age']=review_age

#
# add avg_stars, no. of useful reviews, no. of fans, no. of friends, no. of reviews written of user as feature
#

features['user_avgstars']=data['avgstars']
features['user_usefulcount']=data['user_useful']
features['user_fancount']=data['fans']
features['user_friendscount']=data['friendcount']
features['user_reviewcount']=data['user_reviewcount']

#
# compute yelp experience from yelp start date and review date and add feature
# NOTE: computes experience at the time of writing review
#
userExp=list()
for i in xrange(0,len(data['review_date'])):
	rd=datetime.datetime.strptime(data['review_date'][i], '%Y-%m-%d').date()
	start_date=datetime.datetime.strptime(data['yelp_startdate'][i], '%Y-%m').date()
	userExp.append((rd-start_date).days)

features['user_yelpexp']=userExp

#
# adding review useful binary target and count 
#
#
review_use=list()
for i in xrange(0,len(data['review_useful'])):
	if data['review_useful'][i]>0:
		review_use.append(1)
	else:
		review_use.append(0)

features['review_usefulcount'] = data['review_useful']
features['review_isuseful'] = review_use
# write out updated output.csv
#
#
outfile=open(str(sys.argv[2]),'w')
writer=csv.writer(outfile)
writer.writerow(('review_id','review_rating','review_len','review_numwords','review_numsentences','review_avgnumwords','review_age','user_avgstars','user_usefulcount','user_fancount','user_friendscount','user_reviewcount','user_yelpexp','review_usefulcount','review_isuseful'))
for i in xrange(0,len(features['review_id'])):
	writer.writerow( (features['review_id'][i],features['review_rating'][i],features['review_len'][i],features['review_numwords'][i],features['review_numsentences'][i],features['review_avgnumwords'][i],features['review_age'][i],features['user_avgstars'][i],features['user_usefulcount'][i],features['user_fancount'][i],features['user_friendscount'][i],features['user_reviewcount'][i],features['user_yelpexp'][i],features['review_usefulcount'][i],features['review_isuseful'][i]))
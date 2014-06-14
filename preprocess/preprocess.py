import sys
import json
import re
import csv

#check args
if len(sys.argv) < 3:
	#print str(sys.argv[1])
	print "Args Missing!! \nUsage: preprocess.py <input_file.json> <output_file.csv>"
	exit()

#input file
f=open(str(sys.argv[1]))

#output file
outfile=open(str(sys.argv[2]),'w')
writer=csv.writer(outfile)
writer.writerow(('id','name','review_count','review_id','review_date','stars','text','username','avgstars','user_cool','user_funny','user_useful','fans','friendcount','user_reviewcount','yelp_startdate','review_cool','review_funny','review_useful') )

content=f.readlines()

#
# find number of reviews for each business
#
countList=list()
for i in xrange(0,len(content)):
	if i % 1000 == 0:
		print i
	data=json.loads(content[i])
	if data.get('reviews'):
		countList.append(len(data['reviews']))
	else:
		countList.append(0)

#
# take top 'numEntries' and extract reviews from
# 'restaurantLimit' number of restaurant businesses
# store the result as a csv file
#
numEntries=20
sortedList=sorted(countList)
topEntries=sortedList[-numEntries:]

isRestaurant=False
numRestaurantsFound=0
restaurantsLimit=10
for i in reversed(topEntries):
	topEntry=i
	rIndex=countList.index(topEntry)
	a=json.loads(content[rIndex],encoding='ascii')
	print u"{} ----- {} ----- {} ----- {}".format(rIndex,a['name'], a['review_count'], a['categories'])
	for j in xrange(0,len(a['categories'])):
		matchResult = re.match('restaurant',a['categories'][j],re.I)
		if matchResult:
			print "found restaurant {}".format(a['name'])
			isRestaurant=True
			break
	if isRestaurant:
		print "writing restaurant {}".format(a['name'])
		nreviews=len(a['reviews'])
		for k in xrange(0,nreviews):
			reviewItem=a['reviews'][k]
			rid=reviewItem['review_id']
			rdate=reviewItem['date']
			rstars=reviewItem['stars']
			rtext=reviewItem['text']
			rtext=rtext.encode('ascii',errors='ignore')
			#
			userItem=reviewItem['user']
			ruser_name=userItem['name']
			ruser_name=ruser_name.encode('ascii',errors='ignore')
			ruser_avgstars=userItem['average_stars']
			ruser_cool=userItem['votes']['cool']
			ruser_funny=userItem['votes']['funny']
			ruser_useful=userItem['votes']['useful']
			ruser_fans=userItem['fans']
			ruser_friendcount=userItem['friend_count']
			ruser_reviewcount=userItem['review_count']
			ruser_yelpstart=userItem['yelping_since']
			#
			votesItem=reviewItem['votes']
			review_cool=votesItem['cool']
			review_funny=votesItem['funny']
			review_useful=votesItem['useful']
			#
			writer.writerow( (a['business_id'],a['name'],a['review_count'],rid,rdate,rstars,rtext,ruser_name,ruser_avgstars,ruser_cool,ruser_funny,ruser_useful,ruser_fans,ruser_friendcount,ruser_reviewcount,ruser_yelpstart,review_cool,review_funny,review_useful) )
		isRestaurant=False
		numRestaurantsFound=numRestaurantsFound+1;
		if numRestaurantsFound == restaurantsLimit:
			break

outfile.close()
f.close()

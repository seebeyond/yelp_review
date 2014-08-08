#
# To extract all PCFG features from raw parse
# probabilities obtained from stanford parser
# this also implicitly converts tsv file used 
# for stanford parser back to csv format
import csv
import numpy
import sys

if len(sys.argv) < 3:
    sys.exit("Usage: extract_pcfg_features.py in_useful_file1.tsv in_notusefule_file2.tsv outfile.csv")

infile1=open(sys.argv[1])
inreader1 = csv.reader(infile1,delimiter="\t")

infile2=open(sys.argv[2])
inreader2 = csv.reader(infile2,delimiter="\t")

outfile=file(sys.argv[3], 'w+')
outwriter=csv.writer(outfile)

# TSV files will not have header
# since they are generated from java (parser)
#WRITE HEADER TO CSV FILE
outwriter.writerow(('id','name','review_count','review_id','review_date','stars','text','username','avgstars','user_cool','user_funny','user_useful','fans','friendcount','user_reviewcount','yelp_startdate','review_cool','review_funny','review_useful','parser_sentcount','parser_wordcount','Num_nouns','Num_verbs','Num_advs','Num_adjs','Num_prep','Num_conj','Num_pronouns','Num_modals','Num_articles','SW_nouns','SW_verbs','SW_advs','SW_adjs','SW_prep','Sw_conj','SW_pronouns','SW_modals','SW_articles','min_length','max_length','avg_length','ratio of max to min len','diff_min_prob','diff_max_prob','diff_avg_prob','diff_sdev_prob') )

next(inreader1, None)  
next(inreader2, None)  
empty_count=0
#iterate over rows of csv file
for row_u,row_nu in zip(inreader1, inreader2):
	scores_u=list()
	scores_nu=list()
#for each row extract the parse prob values
	scores=row_u[19].split('$');
	for score in scores:
		if score != '':
			scores_u.append(float(score))
	#print scores
	if scores_u:
#compute all statistics for useful parser
		umin_feature=min(scores_u)
		umax_feature=max(scores_u)
		uavg_feature=sum(scores_u)/len(scores_u)
		#
		unarr=numpy.array(scores_u)
		usdev_feature=numpy.std(unarr,axis=0)
		del(row_u[19])
	else:
		umin_feature=0
		umax_feature=0
		uavg_feature=0
		usdev_feature=0
#	row_u.append(umin_feature)
#	row_u.append(umax_feature)
#	row_u.append(uavg_feature)
#	row_u.append(usdev_feature)

	scores=row_nu[19].split('$');
	for score in scores:
		if score != '':
			scores_nu.append(float(score))
	if scores_nu:
#compute all statistics for not useful parser
		numin_feature=min(scores_nu)
		numax_feature=max(scores_nu)
		nuavg_feature=sum(scores_nu)/len(scores_nu)
		#
		nunarr=numpy.array(scores_nu)
		nusdev_feature=numpy.std(nunarr,axis=0)
	else:
		numin_feeature=0
		numax_feature=0
		nuavg_feature=0
		nusdev_feature=0
		empty_count+=1
#	row_u.append(numin_feature)
#	row_u.append(numax_feature)
#	row_u.append(nuavg_feature)
#	row_u.append(nusdev_feature)

#
#ADDING DIFFERENCE FEATURES
#
	diff_min=umin_feature-numin_feature
	diff_max=umax_feature-numax_feature
	diff_avg=uavg_feature-nuavg_feature
	diff_sdev=usdev_feature-nusdev_feature


	row_u.append(diff_min)
	row_u.append(diff_max)
	row_u.append(diff_avg)
	row_u.append(diff_sdev)

#write row to new csv file
	outwriter.writerow(row_u)

print "Number of score empty instances: ",empty_count
outfile.close();
infile1.close();
infile2.close();

import csv
import sys

if len(sys.argv)<9:
	sys.exit("Usage: python combine_features.py <basic_features.csv> <pcfg_features.csv> <ngram_feature1.tsv> <ngram_feature2.tsv> <ngram_feature3.tsv> <ngram_feature4.tsv> <sentiment_feature.csv> <outfile.csv>")
	
BASIC_FEATURES_LIST=[1,2,5,6,7,8,9,10,11,12]
TARGET_INDEX = 14
PCFG_FEATURES_LIST=range(19,47)
NGRAM_FEATURES_INDEX=19
SENT_FEATURE_INDEX=1

BASIC_FEATURES=sys.argv[1]
PCFG_FEATURES=sys.argv[2]
NGRAM_FEATURES_1=sys.argv[3]
NGRAM_FEATURES_2=sys.argv[4]
NGRAM_FEATURES_3=sys.argv[5]
NGRAM_FEATURES_4=sys.argv[6]
SENT_FEATURES=sys.argv[7]
OUTFILE=sys.argv[8]

basic_f = open(BASIC_FEATURES)
pcfg_f = open(PCFG_FEATURES)
ngram_f1 = open(NGRAM_FEATURES_1)
ngram_f2 = open(NGRAM_FEATURES_2)
ngram_f3 = open(NGRAM_FEATURES_3)
ngram_f4 = open(NGRAM_FEATURES_4)
sent_f = open(SENT_FEATURES)
outfile=open(OUTFILE,'w')

basic_reader=csv.reader(basic_f)
pcfg_reader=csv.reader(pcfg_f)
ngram_reader1=csv.reader(ngram_f1,delimiter="\t")
ngram_reader2=csv.reader(ngram_f2,delimiter="\t")
ngram_reader3=csv.reader(ngram_f3,delimiter="\t")
ngram_reader4=csv.reader(ngram_f4,delimiter="\t")
sent_reader=csv.reader(sent_f)
output_writer=csv.writer(outfile)

basic_reader.next()
pcfg_reader.next()
cnt=1
header=list()

header.extend( ("review_rating","review_len","review_avgnumwords","review_age","user_avgstars", "user_usefulcount","user_fanscount","user_friendscount","user_reviewcount","user_yelpexp","parser_sentcount","parser_wordcount","Num_nouns","Num_verbs","Num_advs","Num_adjs","Num_prep","Num_conj","Num_pronouns","Num_modals","Num_articles","SW_nouns","SW_verbs","SW_advs","SW_adjs","SW_prep","SW_conj","SW_pronouns","SW_modals","SW_articles","sent_minlen","sent_maxlen","sent_avglen","sent_lenratio","diff_min_prob","diff_max_prob","diff_avg_prob","diff_sdev_prob","tgword","tgchar","bgword","bgchar","sent_score","target" ) )
output_writer.writerow(header);
for brow,prow,twrow,tcrow,bwrow,bcrow,sentrow in zip(basic_reader,pcfg_reader,ngram_reader1,ngram_reader2,ngram_reader3,ngram_reader4,sent_reader):
#	print len(tcrow)
	nrow=list()
	for index in BASIC_FEATURES_LIST:
		nrow.append(brow[index])
	for index in PCFG_FEATURES_LIST:
		nrow.append(prow[index])
	#
	nrow.append(twrow[NGRAM_FEATURES_INDEX])
	nrow.append(tcrow[NGRAM_FEATURES_INDEX])
	nrow.append(bwrow[NGRAM_FEATURES_INDEX])	
	nrow.append(bcrow[NGRAM_FEATURES_INDEX])
	#TARGET
	nrow.append(sentrow[SENT_FEATURE_INDEX])	
	nrow.append(brow[TARGET_INDEX])
	output_writer.writerow(nrow)
	cnt=cnt+1
outfile.close()

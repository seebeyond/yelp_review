import sys
import nltk
import csv
from nltk.model import NgramModel
from nltk.probability import LidstoneProbDist
import math

#!!!!! COMPATIBILITY
# nltk version 2.0.4

#USAGE:
#python extract_word_ngram_features.py <N-value> <location of reviews files> <useful_reviews_file> <notuseful_reviews_file <training-data.tsv> <output-file.tsv> 
#corpus reader requires root directory and corpus file to be specified seperately
#arg2 is directory were corpus file is present and arg3,arg4 are exact corpus file names
#NVAL=2
#TRAIN_DATA_PATH="."
#USEFUL_REVIEWS_FILE="dummy.txt"
#NOTUSEFUL_REVIEWS_FILE="raw_notuseful_reviews.txt"
#INPUT_DATA_FILE="training-data.tsv"
#OUTPUT_FILE="out.tsv"

NVAL=int(sys.argv[1])
TRAIN_DATA_PATH=sys.argv[2]
USEFUL_REVIEWS_FILE=sys.argv[3]
NOTUSEFUL_REVIEWS_FILE=sys.argv[4]
INPUT_DATA_FILE=sys.argv[5]
OUTPUT_FILE=sys.argv[6]

print "Creating ",NVAL,"-gram models"
outfile=open(OUTPUT_FILE,'w')
writer=csv.writer(outfile,delimiter="\t")

myCorpusReader = nltk.corpus.reader.PlaintextCorpusReader(TRAIN_DATA_PATH,USEFUL_REVIEWS_FILE)
myCorpus = [word.lower() for word in myCorpusReader.words()]

# Remove rare words from the corpus
fdist = nltk.FreqDist(w for w in myCorpus)
vocabulary = set(map(lambda x: x[0], filter(lambda x: x[1] >= 5, fdist.iteritems())))

myCorpus = map(lambda x: x if x in vocabulary else "*unknown*", myCorpus)


estimator = lambda fdist, bins: LidstoneProbDist(fdist, 0.2) 
lm_useful = NgramModel(NVAL, myCorpus, estimator=estimator)
print "Useful reviews model complete"

myCorpusReader = nltk.corpus.reader.PlaintextCorpusReader(TRAIN_DATA_PATH,NOTUSEFUL_REVIEWS_FILE)
myCorpus = [word.lower() for word in myCorpusReader.words()]

# Remove rare words from the corpus
fdist = nltk.FreqDist(w for w in myCorpus)
vocabulary = set(map(lambda x: x[0], filter(lambda x: x[1] >= 5, fdist.iteritems())))

myCorpus = map(lambda x: x if x in vocabulary else "*unknown*", myCorpus)


estimator = lambda fdist, bins: LidstoneProbDist(fdist, 0.2)
lm_notuseful = NgramModel(NVAL, myCorpus, estimator=estimator)
print "Not Useful reviews model complete"

print "Generating features for input data"
f=open(INPUT_DATA_FILE)
reader = csv.reader(f,delimiter="\t")
cnt=1
for row in reader:
	#nltk.word_tokenize(row[6])
	#print cnt
	text=row[6].replace('.', ' . ')
	text=text.replace('\'',' ')
	words = nltk.word_tokenize(text)
	words = [word.lower() for word in words]
	if NVAL==1:
		tgrams=words
	elif NVAL==2:
		tgrams=nltk.bigrams(words)
	elif NVAL ==3:
		tgrams=nltk.trigrams(words)
	else:
		print "ONLY SUPPORTED FOR BIGRAM AND TRIGRAM"
	review_useful_lprob=0
	review_notuseful_lprob=0
	for tgram in tgrams:
		#print tgram
		index=NVAL-1
		prob_useful=lm_useful.prob(tgram[index],tgram[:index])
		prob_notuseful=lm_notuseful.prob(tgram[index],tgram[:index])
		if prob_useful<1 and prob_notuseful<1:
			review_useful_lprob+=math.log(prob_useful)
			review_notuseful_lprob+=math.log(prob_notuseful)
	diff=review_useful_lprob-review_notuseful_lprob
	#decided not to take absolute value for difference features
	#should research the effect of abs value on modeling
	row.append(diff)
	writer.writerow(row)
	cnt+=1

outfile.close()
f.close()
print "Feature generation complete"

#ANALYSIS OF INVALID NGRAMS
#count_common=0
#count_unique=0	
#for elem in set_invalid:
#	if elem in set_invalid_useful:
#		count_common+=1
#	else:
#		count_unique+=1	
#
#print count_common,count_unique
#count_common=0
#count_unique=0	
#for elem in set_invalid_useful:
#	if elem in set_invalid:
#		count_common+=1
#	else:
#		count_unique+=1
#print count_common,count_unique	
#!/usr/local/bin/python
import csv
import sys
import numpy
import nltk.stem.porter
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import re
import itertools

class StemmingTokenizer(object):
	def __init__(self):
		self.stemmer = nltk.stem.porter.PorterStemmer()

	def __call__(self, doc):
		tokens = re.findall(r'(?u)\b[\w\'-]+\b', doc)
		stemmed = [self.stemmer.stem(token) for token in tokens]
		return [re.sub(r"_+\b", "", token) for token in stemmed]

def preprocess(doc):
	doc = doc.lower()
	# Change hyphen and apostrophe inside a word to underscore.
	doc = re.sub(r"(\w)[-'](\w)", "\\1_\\2", doc)
	doc = re.sub(r"(\w)[-'](\w)", "\\1_\\2", doc) # hack for e.g. "8-1-9"
	# Replace all non-underscore punctuation with a space.
	doc = re.sub(r"[^\w\s_]", " ", doc)
	# Remove underscores at the beginning/end of tokens.
	doc = re.sub(r"_+\b", "", doc)
	doc = re.sub(r"\b_+", "", doc)
	# Collapse whitespace.
	doc = re.sub(r"\s+", " ", doc)
#	print doc
	return doc.strip()

def build_vectorizer(remove_stop_words=False, stem=False):
	stop_words = 'english' if remove_stop_words else None
	tokenizer = StemmingTokenizer() if stem else None
	vectorizer = CountVectorizer(
		token_pattern=r'(?u)\b[\w\'-]+\b',
		stop_words=stop_words,
		preprocessor=preprocess,
		tokenizer=tokenizer)
	return vectorizer

if len(sys.argv) < 2:
    sys.exit("Usage: extract_baseline_tfidf_features.py training_file.csv outfile.csv")

#
# get args and load corpus variable
#
TRAINING_DATA=sys.argv[1]
OUTFILE=sys.argv[2]

#the column number of review text
REVIEW_FIELD_ID=6

train_file = open(TRAINING_DATA)
outfile=open(OUTFILE,'w')

train_reader=csv.reader(train_file)

header=train_reader.next()

corpus=list()
counter=1
for row in train_reader:
#	print row[REVIEW_FIELD_ID]
	corpus.append(row[REVIEW_FIELD_ID])
	counter+=1
	#if(counter==1001):
	#	break


vectorizer = build_vectorizer(remove_stop_words=True, stem=True)
train_features = vectorizer.fit_transform(corpus)
count_array = train_features.toarray()
transformer = TfidfTransformer()
tfidf_features = transformer.fit_transform(count_array)
tfidf_array=tfidf_features.toarray()

token_names=vectorizer.get_feature_names()
#rows, cols = tfidf_features.nonzero() 


#
#output file
outfile=open(OUTFILE,'w')
writer=csv.writer(outfile)

writer.writerow(token_names)
for row in tfidf_array:
	record=list()
	for entry in row:
		record.append(entry)
	writer.writerow(record)

outfile.close()


#for token in token_names:
#	print token

#print len(token_names)

#for i,j in itertools.izip(rows,cols):
#	print token_names[j], tfidf_features[i,j]
#row=list()
#for i in xrange(0,len(corpus)):
#	for j in xrange(0,len(token_names)):
#		if i in rows and j in cols:
#			row.append(tfidf_features[i,j])
#		else:
#			row.append(0.0)
#writer.writerow(row)		
##print tfidf_array 

#!/bin/sh

# ARG1 - path to sentiment wordnet
# ARG2 - parser path
# ARG3 - location of train data
# ARG4 - location of output file

#echo $1
java -Xmx15000m -jar ../../data-restaurants/sentiment-tool-lib/sentiment_scorer.jar  $1  $2  $3  $4
echo "done"

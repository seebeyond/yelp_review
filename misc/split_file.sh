#!/bin/sh

#USAGE: ./split_file.sh <FILENAME> <CHUNKSIZE>
FILE=$1
CHUNKSIZE=$2

a=`wc -l $FILE`

split -l $CHUNKSIZE  -d $FILE "part"

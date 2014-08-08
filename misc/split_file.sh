#!/bin/sh

#USAGE: ./split_file.sh <FILENAME> <CHUNKSIZE> <PREFIX>
FILE=$1
CHUNKSIZE=$2
PREFIX=$3

a=`wc -l $FILE`

split -l $CHUNKSIZE  -d $FILE $PREFIX

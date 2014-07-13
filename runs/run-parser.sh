#!/bin/sh

# ARG1 - cmd - "parse"/"train"
# ARG2 - location of parser
# ARG3 - location of input file
# ARG4 - location of output file

#echo $1
java -Xmx15000m -jar ../../data/parsers/yp.jar  $1  $2  $3  $4
echo "done"

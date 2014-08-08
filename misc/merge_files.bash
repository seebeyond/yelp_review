#!/bin/bash

#ARG1 - file_name_prefix
#ARG2 - file_name_suffix_end (assumed to start from 00)
#ARG3 - outfile_name

input_file_name=$1
end_limit=$2
output_file_name=$3

touch output_file_name
d=1
for i in $(seq -f "%02g" 0 $2)
do
	fn="$input_file_name$i.tsv"
	lines=`wc -l < $fn`
	rlines=$(expr $lines - $d)
	tail -$rlines $fn  >> $output_file_name
done

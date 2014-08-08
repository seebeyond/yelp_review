#!/bin/bash

#ARG1 - last suffix


# ./condorizer-16G.py ./run-parser.sh "parse" ../../../data-restauran^C/parsers/usefulReviewParser_threshold.ser.gz ../../../data-restaurants/split-data/80-20/test/chunks/part-testing-data06 ../../../data-restaurants/test-data-features/pcfg-features/80-20/raw/useful-chunks/raw_pcfg_useful06.tsv useful_parse06.out

for i in $(seq -f "%02g" 0 $1)
do
	#echo $i 
	#echo ${fseq[$i]}
	input_file="../../../data-restaurants/split-data/80-20/test/chunks/part-testing-data$i"
	log_file="notuseful_parse$i.out"
	output_file="../../../data-restaurants/test-data-features/pcfg-features/80-20/raw/notuseful-chunks/raw_pcfg_notuseful$i.tsv"
	echo "Submitting job for input: $input_file"
	./condorizer-16G.py ./run-parser.sh "parse" ../../../data-restaurants/parsers/notusefulReviewParser.ser.gz $input_file $output_file $log_file

done

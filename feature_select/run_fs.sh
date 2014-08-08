#!/bin/sh

# ARG1 - script name
# ARG2 - train input file
# ARG3 - model name
# ARG4 - outfile

alias rscript=/lusr/opt/R-3.0.3/bin/Rscript
rscript $1 $2 $3 > $4
echo "done"


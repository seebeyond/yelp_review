Detecting Useful Business Reviews using Stylometric Features
============================================================

This repo contains code required to reproduce experiments
in the paper titled:
 
"Detecting Useful Business Reviews using Stylometric Features"

It presents an approach to detect useful business reviews 
using stylometric features. We train n-gram and PCFG models to
capture writing style and structural patterns and employ them in 
extracting useful features from review text. Using Yelp dataset,
we demonstrate that useful reviews have distinct style of writing 
that can be utilized in detecting them and empirically evaluate 
the same.We report improved accuracy compared to using just lexical 
or bag of words features. We also find that domain of business 
reviews do not affect the importance of stylometric features.

### Data:

Data to reproduce the experiments in the paper is shared at:

http://www.cs.utexas.edu/~vidhoon/data-review-exp.zip

Please refer to README inside for details.
The README is also found in data/ folder in this repo to avoid
downloading entire data. Last time I checked, size was 1GB (approx).

### Languages:

Components are coded in python, JAVA and some tools are written 
in shell/bash scripts.

### CITATION:

Please cite this paper if you happen to re use code or preprocessed/
processed Yelp review data from this project:

Vidhoon Viswanathan, Raymond Mooney, Joydeep Ghosh, "Detecting useful
business reviews using Stylometric Features" (submitted to Yelp Data contest)

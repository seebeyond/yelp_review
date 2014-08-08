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


CITATION:
========

Please cite this paper if you happen to re use code or preprocessed/
processed Yelp review data from this project:

Vidhoon Viswanathan, Raymond Mooney, Joydeep Ghosh, "Detecting useful
business reviews using Stylometric Features" (submitted to Yelp Data contest)

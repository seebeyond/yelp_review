# Common R script to do CV training
# and print confusion matrix for different
# models.
# Usage:
# arg1 - data.csv
# arg2 - model name (according to caret package)
#

# MAPPING OF MODEL NAME for caret package
# decision tree - rpart
# linear svm - svmLinear
# radial svm - svmRadial
# logistic regression - plr
# naive bayes - nb
# k-nearest - knn
# tree ensemble - treebag
# boosted tree - ada
# boosted logistic - LogitBoost

require(caret)
#caret auto loads required package based on model 
#require(rpart)
#require(kernlab)
#require(glmnet)
#require(klaR)

set.seed(10)
#commandArgs <- function() { c("...") }

args = commandArgs(TRUE)
data = read.csv(args[1], sep = ",", header = TRUE, na.strings = "")
data=na.omit(data)
data=data.frame(data)

trainData=data[,-ncol(data)]
trainTarget=data[,ncol(data)]
trainTarget=as.factor(trainTarget)
levels(trainTarget)=c("no","yes")

#feature selection
#normalization <- preProcess(trainData)
#trainData <- predict(normalization, trainData)
#trainData <- as.data.frame(trainData)
subsets <- c(5,10,15,20,25,30,40)

ctrl = rfeControl(functions = caretFuncs)
fProfile <- rfe(trainData, trainTarget,
                 sizes = subsets,
                 rfeControl = ctrl, method = args[2])

print(fProfile)


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
#subsets <- c(1:10)

#fitcontrol for ROC metric
fitControl <- trainControl(method = "cv", 
				classProbs = TRUE, 
				summaryFunction = twoClassSummary )

#fitcontrol for ACC metric
#fitControl <- trainControl(method = "cv")
reviewModel = train(x=trainData, y=trainTarget, 
			method = args[3],
			tuneLength = 50,
			trControl = fitControl,
			metric="ROC")

print(reviewModel)
print(confusionMatrix(reviewModel,'average'))

test_data = read.csv(args[2], sep = ",", header = TRUE, na.strings = "")
test_data=na.omit(test_data)
test_data=data.frame(test_data)

testData=test_data[,-ncol(test_data)]
testTarget=test_data[,ncol(test_data)]
testTarget=as.factor(testTarget)
#print(levels(testTarget))
levels(testTarget)=c("no","yes")

testOut=predict(reviewModel,testData)

testlen=length(testTarget)
ncorrect=length(which(testOut==testTarget))
testAcc=ncorrect/testlen

print(c("test accuracy: ",testAcc))

from pyspark.mllib.classification import LogisticRegressionWithLBFGS, LogisticRegressionModel
from pyspark import SparkContext
from fileinput import input
from pyspark.mllib.linalg import Vectors
from pyspark.mllib.regression import LabeledPoint
from glob import glob
from pyspark.mllib.util import MLUtils
from pyspark.sql import SQLContext, Row
from pyspark.sql.types import *
from pyspark.ml.feature import HashingTF,IDF,Tokenizer


sc=SparkContext("local","dd")
sqlContext = SQLContext(sc)

#lines = sc.textFile("/home/ankita/MLProject/data/OriginalTraining.txt")
lines=sc.textFile("/Users/admin/Desktop/KBSApp/KBSApp/permissionsData/dataSets/SVMDataSet.txt")

parts = lines.map(lambda l: l.split(","))
f = parts.map(lambda p: Row(tindex=int(p[0]),packageName=p[1],packagePermissions=p[2], label= int(float(p[3])),training=1))


linest = sc.textFile("/Users/admin/Desktop/KBSApp/KBSApp/permissionsData/dataSets/SVMDataGroundTruth.txt")
partst = linest.map(lambda l: l.split(","))
ft = partst.map(lambda p: Row(tindex=int(p[0]),packageName=p[1],packagePermissions=p[2],label= int(float(p[3])),training=0))
alldata = f.union(ft)

schemaApp = sqlContext.createDataFrame(alldata)

schemaApp.registerTempTable("data")

tokenizer = Tokenizer(inputCol="packagePermissions", outputCol="perms")
permsData = tokenizer.transform(schemaApp)

hashingTF = HashingTF(inputCol="perms", outputCol="rawFeatures")
featurizedData = hashingTF.transform(permsData)


idf = IDF(inputCol="rawFeatures", outputCol="features")


idfModel = idf.fit(featurizedData)
rescaledData = idfModel.transform(featurizedData)

wordsvectors = rescaledData["label","features"].map(lambda row: LabeledPoint(row[0], row[1]))
model = LogisticRegressionWithLBFGS.train(wordsvectors, iterations=100)

labelsAndPreds = wordsvectors.map(lambda p: (p.label, model.predict(p.features)))

trainErr = labelsAndPreds.filter(lambda (v, p): v != p).count() / float(wordsvectors.count())
print("Training Error = " + str(trainErr))

resct=rescaledData.filter(rescaledData.training==0)
print("*********************************************************")
print(rescaledData.take(35))
print(labelsAndPreds.take(35))
print("*********************************************************")

labelsAndPreds =resct.map(lambda p: (p.label, model.predict(p.features)))
trueneg = labelsAndPreds.filter(lambda (v,p): v==0 and p==0).count() 
#print("*********************************************************")
#print(rescaledData.take(25))
#print(trueneg.take(25))
print("*********************************************************")

falseneg = labelsAndPreds.filter(lambda (v,p): v==1 and p==0).count() 
truepos = labelsAndPreds.filter(lambda (v,p): v==1 and p==1).count()
falsepos = labelsAndPreds.filter(lambda (v,p): v==0 and p==1).count()

print("false negative:", falseneg)
print("false positive:", falsepos)
print("true negative:", trueneg)
print("true positive:", truepos)
print("Fscore:", float(2*truepos)/(2*truepos + falsepos + falseneg))
print("Test Error = ", float(falseneg + falsepos)/resct.count())
#model.save(sc, "/home/ankita/MLProject/SVM/myModelPath")

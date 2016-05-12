from nltk.classify import NaiveBayesClassifier
from nltk.corpus import subjectivity
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.sentiment.util import *
from textblob import TextBlob
import codecs


data=[]
fileName="/Users/admin/Desktop/KBSApp/KBSApp/tutorial/tutorial/spiders/scrapedAppReviews/allReviews.txt"
with codecs.open(fileName,"r",encoding='utf-8') as f:
    for line in f:
        if line and line.strip():
            data.append(line)

print(len(data))


textblb = []
for i in data:
    textblb.append(TextBlob(i))

sentiments=[]
for i in textblb:
    sentiments.append(i.sentiment)

polarities=[]
for i in sentiments:
    polarities.append(i[0])

labels=[]
for i in polarities:
     if i>0.0:
         labels.append("pos")
     else:
         labels.append("neg")

labeled_data = []
for i in range(len(data)):
    content=data[i]+","+labels[i]+","+str(polarities[i])+"\n"
    with codecs.open("/Users/admin/Desktop/KBSApp/KBSApp/tutorial/tutorial/spiders/scrapedAppReviews/allReviewSentiments.txt","a",encoding='utf-8') as out:
        out.write(content)
    
    out.close

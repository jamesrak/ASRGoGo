#coding=utf-8
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from gensim.models import Word2Vec
import pickle

Y = [] #list of label
df = [] #dataset of words each row
listOfword = [] #list of unique word
#----------------------------------get data from dev set time.txt----------------------------------
texts = open("train_set.txt",'r', encoding='utf-8')
for text in texts :
    # -----------split all words in string to list----------------
    words = text.split()
    df.append(words)
    Y.append(0)
    listOfword += words

#----------------------------------get data from dev what time.txt----------------------------------
texts = open("train_time.txt",'r', encoding='utf-8')
for text in texts :
    # -----------split all words in string to list----------------
    words = text.split()
    df.append(words)
    Y.append(1)
    listOfword += words

#----------------------------------get data from dev postpone .txt----------------------------------
texts = open("train_postpone.txt",'r', encoding='utf-8')
for text in texts :
    # -----------split all words in string to list----------------
    words = text.split()
    df.append(words)
    Y.append(2)
    listOfword += words

#----------------------------------get data from dev postpone .txt----------------------------------
texts = open("train_task.txt",'r', encoding='utf-8')
for text in texts :
    # -----------split all words in string to list----------------
    words = text.split()
    df.append(words)
    Y.append(3)
    listOfword += words

#---------------make listOfword to unique------------------------
listOfword = list(set(listOfword))
print(listOfword)
#------------------store listOfword into file listOfWord.txt--------------------------------
stringList = ','.join(listOfword)
fileList = open("listOfWord.txt",'w', encoding='utf-8')
fileList.write(stringList)
fileList.close()

#----------------------make frequency dataset from words-----------------------------------
count = []
for i in df:
    row = []
    for l in listOfword :
        w = 0
        for j in i :
            if(j==l) : w+=1
        row.append(w)
    count.append(row)
#----------------------train tfidf from data and store---------------------------------------------
transformer = TfidfTransformer(smooth_idf=False)
tfidf = transformer.fit_transform(count)
pickle._dump(transformer,open("transformer.sav",'wb'))

#----------------------train word2vec from data and store-------------------------------------------
word2vecModel = Word2Vec(df, size=50, window=4, min_count=2)
# pickle._dump(transformer,open("transformer.sav",'wb'))
print(word2vecModel.wv['ตื่น'])

#----------------------train model from data and store---------------------------------------------
clf = MultinomialNB()
clf.fit(tfidf,Y)
pickle._dump(clf,open("clf.sav",'wb'))
#-----------------------get predicted label from model-----------------------------------
y_pred = clf.predict(tfidf)
print(y_pred)
print(Y)

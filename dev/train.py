#coding=utf-8
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
import pickle
# In[1]
Y = [] #list of label
df = [] #dataset of words each row
#----------------------------------get data from dev set time.txt----------------------------------
texts = open("train_set.txt",'r', encoding='utf-8')
for text in texts :
    # -----------split all words in string to list----------------
    words = text.split()
    df.append(text.replace('\n',''))
    Y.append(0)

#----------------------------------get data from dev what time.txt----------------------------------
texts = open("train_time.txt",'r', encoding='utf-8')
for text in texts :
    # -----------split all words in string to list----------------
    words = text.split()
    df.append(text.replace('\n',''))
    Y.append(1)

#----------------------------------get data from dev postpone .txt----------------------------------
texts = open("train_postpone.txt",'r', encoding='utf-8')
for text in texts :
    # -----------split all words in string to list----------------
    words = text.split()
    df.append(text.replace('\n',''))
    Y.append(2)

#----------------------------------get data from dev postpone .txt----------------------------------
texts = open("train_task.txt",'r', encoding='utf-8')
for text in texts :
    # -----------split all words in string to list----------------
    words = text.split()
    df.append(text.replace('\n',''))
    Y.append(3)
# In[2]

#----------------------make frequency dataset from words-----------------------------------
def token(x):
    return x.split(' ')
countT = CountVectorizer(min_df=1,ngram_range=(1, 1), tokenizer=token)
countT.fit_transform(df)
pickle._dump(countT, open("countT.sav",'wb'))
count = countT.transform(df)

#----------------------train model from data and store---------------------------------------------
clf = MultinomialNB()
clf.fit(count,Y)
pickle._dump(clf,open("clf.sav",'wb'))
# In[3]
#-----------------------get predicted label from model-----------------------------------
y_pred = clf.predict(count)
print(y_pred)
print(Y)

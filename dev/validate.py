import pickle
from sklearn.metrics import f1_score
from sklearn.metrics import accuracy_score
import pandas as pd
#-----------------------read model------------------------------
model = pickle.load(open("clf.sav","rb"))
tfidf = pickle.load(open("transformer.sav","rb"))
#-----------------------read list of all words------------------
listOfword = open("listOfWord.txt",'r',encoding='utf-8').read().split(',')

Y = [] #list of label
df = [] #dataset of words each row
#----------------------------------get data from dev set time.txt----------------------------------
texts = open("dev_set.txt",'r', encoding='utf-8')
for text in texts :
    # -----------split all words in string to list----------------
    words = text.split()
    df.append(words)
    Y.append(0)

#----------------------------------get data from dev what time.txt----------------------------------
texts = open("dev_time.txt",'r', encoding='utf-8')
for text in texts :
    # -----------split all words in string to list----------------
    words = text.split()
    df.append(words)
    Y.append(1)

#----------------------------------get data from dev postpone .txt----------------------------------
texts = open("dev_postpone.txt",'r', encoding='utf-8')
for text in texts :
    # -----------split all words in string to list----------------
    words = text.split()
    df.append(words)
    Y.append(2)

#----------------------------------get data from dev postpone .txt----------------------------------
texts = open("dev_task.txt",'r', encoding='utf-8')
for text in texts :
    # -----------split all words in string to list----------------
    words = text.split()
    df.append(words)
    Y.append(3)

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


#-----------------------------------apply transform------------------------------------------------
a = tfidf.transform(count)

#-----------------------------------apply model------------------------------------------------
y_pred = model.predict(a)
test_df = pd.DataFrame([y_pred, Y])
print(test_df)
print(y_pred,Y)
f1 = f1_score(Y, y_pred, average='macro')
print(f1)
score = accuracy_score(Y, y_pred)
print(score)

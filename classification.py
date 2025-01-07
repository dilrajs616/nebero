import pandas as pd
import numpy as np
from sklearn import linear_model
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
import matplotlib.pyplot as plt
from numpy import array
from numpy import argmax
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_selection import chi2
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import Dense, Activation
# from tensorflow.keras.utils import to_categorical
# import re
# from tensorflow.keras.preprocessing import sequence
# from tensorflow.keras.preprocessing.text import one_hot
# from tensorflow.keras.preprocessing.text import text_to_word_sequence

from sklearn.svm import LinearSVC


names=['URL','Category']
df=pd.read_csv('./URL Classification.csv',names=names, na_filter=False)
df1 = df[1:2001]
df2 = df[50000:52000]
df3 = df[520000:522000]
df4 =df[535300:537300]
df5 = df[650000:652000]
df6= df[710000:712000]
df7=  df[764200:766200]
df8=  df[793080:795080]
df9=  df[839730:841730]
df10=  df[850000:852000]
df11=  df[955250:957250]
df12=  df[1013000:1015000]
df13=  df[1143000:1145000]
df14=  df[1293000:1295000]
df15=  df[1492000:1494000]
#df6 = df[77000:1562978]
dt=pd.concat([df1,df2,df3,df4,df5,df6,df7,df8,df9,df10,df11,df12,df13,df14,df15], axis=0)
df.drop(df.index[1:2000],inplace= True)
df.drop(df.index[50000:52000],inplace= True)
df.drop(df.index[520000:522000],inplace= True)
df.drop(df.index[535300:537300],inplace= True)
df.drop(df.index[650000:652000],inplace= True)
df.drop(df.index[710000:712000],inplace= True)
df.drop(df.index[764200:766200],inplace= True)
df.drop(df.index[793080:795080],inplace= True)
df.drop(df.index[839730:841730],inplace= True)
df.drop(df.index[850000:852000],inplace= True)
df.drop(df.index[955250:957250],inplace= True)
df.drop(df.index[1013000:1015000],inplace= True)
df.drop(df.index[1143000:1145000],inplace= True)
df.drop(df.index[1293000:1295000],inplace= True)
df.drop(df.index[1492000:1494000],inplace= True)
df.tail()

df.Category.value_counts().plot(figsize=(12,5),kind='bar',color='green');
plt.xlabel('Category')
plt.ylabel('Total Number Of Individual Category for Training')

dt.Category.value_counts().plot(figsize=(12,5),kind='bar',color='green');
plt.xlabel('Category')
plt.ylabel('Total Number Of Individual Category for Testing')

X_train=df['URL']
y_train=df['Category']
#print(X_train)
X_train.shape

X_test=dt['URL']
y_test=dt['Category']
#print(X_test)
X_test.shape


from sklearn.pipeline import Pipeline
text_clf = Pipeline([('vect', CountVectorizer()), ('tfidf', TfidfTransformer()), ('clf', MultinomialNB())])
text_clf = text_clf.fit(X_train, y_train)

from sklearn.model_selection import RandomizedSearchCV
n_iter_search = 5
parameters = {'vect__ngram_range': [(1, 1), (1, 2)], 'tfidf__use_idf': (True, False), 'clf__alpha': (1e-2, 1e-3)}
gs_clf = RandomizedSearchCV(text_clf, parameters, n_iter = n_iter_search)
gs_clf = gs_clf.fit(X_train, y_train)

#X_train, X_test, y_train, y_test = train_test_split(df['URL'], df['Category'],test_size=0.3, random_state = 0)

#y=np.array(df[names[1]])
#print(y)

#from sklearn.pipeline import Pipeline
#from sklearn.multiclass import OneVsRestClassifier
#from nltk.corpus import stopwords
#stop_words = set(stopwords.words('english'))

#text_clf = Pipeline([('vect', CountVectorizer()), ('tfidf', TfidfTransformer()), ('clf', MultinomialNB())])
#text_clf = Pipeline([('vect', CountVectorizer()), ('tfidf', TfidfTransformer()), ('clf', OneVsRestClassifier(MultinomialNB(fit_prior=True, class_prior=None)))])
#text_clf= Pipeline([
                #('tfidf', TfidfVectorizer(stop_words=stop_words)),
                #('clf', OneVsRestClassifier(MultinomialNB(
                   # fit_prior=True, class_prior=None))),
            #])
#text_clf = text_clf.fit(X_train, y_train)
#test_clf =text_clf.fit(X_test, y_test)

#text_clf.get_params().keys()

#from sklearn.model_selection import RandomizedSearchCV
#n_iter_search = 5
#parameters = {'vect__ngram_range': [(1, 1), (1, 2)], 'tfidf__use_idf': (True, False), 'clf__estimator__alpha': (1e-2, 1e-3)}
#parameters = {'tfidf__ngram_range': [(1, 1), (1, 2)], 'tfidf__use_idf': (True, False), 'clf__estimator__alpha': (1e-2, 1e-3)}
#gs_clf = RandomizedSearchCV(text_clf, parameters, n_iter = n_iter_search)
#gs_clf = gs_clf.fit(X_train, y_train)

#print(X_test)

from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import confusion_matrix
#grid_mean_scores = [result.mean_validation_score for result in gs_clf.grid_scores_]
#print(grid_mean_scores)
y_pred=gs_clf.predict(X_test)
precision_recall_fscore_support(y_test, y_pred, average='weighted')

y_pred=gs_clf.predict(X_test)
from sklearn.metrics import classification_report
print(classification_report(y_test, y_pred))

print(classification_report(y_test, y_pred, digits=4))

import seaborn as sn
import matplotlib.pyplot as plt
import numpy as np


array = confusion_matrix(y_test, y_pred)
cm=np.array(array)
cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
df_cm = pd.DataFrame(cm, index = [i for i in "0123456789ABCDE"],
                  columns = [i for i in "0123456789ABCDE"])
plt.figure(figsize = (20,15))
sn.heatmap(df_cm, annot=True)


print(gs_clf.predict(['https://vuejs.org/']))
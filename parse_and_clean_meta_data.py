# based on https://colab.research.google.com/drive/1Zv6MARGQcrBbLHyjPVVMZVnRWsRnVMpV
#!/usr/bin/env python
# coding: utf-8

# In[1]:


import itertools
import os
import json
import gzip
import pandas as pd
from urllib.request import urlopen


# In[12]:


get_ipython().system('wget http://jmcauley.ucsd.edu/data/amazon_v2/categoryFilesSmall/Kindle_Store_5.json.gz')


# In[2]:


### load the meta data

data = []
with gzip.open('Kindle_Store_5.json.gz') as f:
    for l in f:
        data.append(json.loads(l.strip()))
    
# total length of list, this number equals total number of products
print(len(data))

# first row of the list
print(data[0])


# In[3]:


# convert list into pandas dataframe

df = pd.DataFrame.from_dict(data)

print(len(df))


# In[4]:


df.head


# In[5]:


df_relevant_columns = df.loc[:, ["overall", "reviewText"]]


# In[6]:


df_relevant_columns.dropna(inplace=True)


# In[7]:


df_relevant_columns.head


# In[8]:


df_relevant_columns.columns


# In[9]:


reviews = df_relevant_columns["reviewText"]
sentiment = df_relevant_columns["overall"].apply(
    func=lambda rating: "pos" if rating > 3 else "neg" if rating < 3 else "neutral"
)


# In[10]:


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn import metrics


# In[11]:


reviews_train, reviews_test, sentiment_train, sentiment_test = train_test_split(reviews, sentiment)


# In[12]:


def train_on_different_size(n_samples):
    pipeline = Pipeline([
        ('vect', TfidfVectorizer()),
        ('clf', LinearSVC()),
    ])
    return pipeline.fit(reviews_train.iloc[0:n_samples], sentiment_train.iloc[0:n_samples])


# In[13]:


pipeline_5000 = train_on_different_size(5000)
print(pipeline_5000.score(reviews_test.iloc[0:10000], sentiment_test.iloc[0:10000]))


# In[14]:


pipeline = train_on_different_size(10000)
print(pipeline.score(reviews_test.iloc[0:10000], sentiment_test.iloc[0:10000]))


# In[15]:


pipeline = train_on_different_size(15000)
print(pipeline.score(reviews_test.iloc[0:10000], sentiment_test.iloc[0:10000]))


# In[16]:


pipeline = train_on_different_size(20000)
print(pipeline.score(reviews_test.iloc[0:10000], sentiment_test.iloc[0:10000]))


# In[25]:


pipeline = train_on_different_size(25000)
print(pipeline.score(reviews_test.iloc[0:10000], sentiment_test.iloc[0:10000]))


# In[26]:


pipeline = train_on_different_size(30000)
print(pipeline.score(reviews_test.iloc[0:10000], sentiment_test.iloc[0:10000]))


# In[109]:


pipeline = train_on_different_size(50000)
print(pipeline.score(reviews_test.iloc[0:10000], sentiment_test.iloc[0:10000]))


# In[110]:


pipeline = train_on_different_size(100000)
print(pipeline.score(reviews_test.iloc[0:10000], sentiment_test.iloc[0:10000]))


# In[111]:


pipeline = train_on_different_size(300000)
print(pipeline.score(reviews_test.iloc[0:10000], sentiment_test.iloc[0:10000]))


# In[112]:


pipeline = train_on_different_size(500000)
print(pipeline.score(reviews_test.iloc[0:10000], sentiment_test.iloc[0:10000]))


# In[ ]:


# TASK: Predict the outcome on the testing set and store it in a variable
# named y_predicted
y_predicted = pipeline.predict(docs_test)

# Print the classification report
print(metrics.classification_report(y_test, y_predicted,
                                    target_names=dataset.target_names))

# Print and plot the confusion matrix
cm = metrics.confusion_matrix(reviews_test, sentiment_test)
print(cm)


import os
import pandas as pd
import nltk
import re

'''
Make sure to install the nltk before hand
'''
from nltk.stem import WordNetLemmatizer
from nltk.stem.snowball import EnglishStemmer
from nltk.tokenize import word_tokenize

'''
Remove these download line if they are already downloaded in my case I need to download it
'''
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('punkt')


'''
Just declaring the Number of files variable
'''
NUMBER_OF_FILES = 0
ratings = pd.DataFrame


'''
Retriving the file names with the help of os module
'''
data_file_names = os.listdir('./DataPickles/')

'''
Write the directory scructure you have for the dataset, and if in the same folder just comment and ignore the below cell
'''
data_file_names = [f'./DataPickles/{file_names}' for file_names in data_file_names]

'''
Initializing the Number of files variable can be useful later
'''
NUMBER_OF_FILES = len(data_file_names)

'''
Routine that converts a five star rating into three categories: 
negative, neutral and positive
'''
def convert_star_rating(rating: pd.DataFrame):
    converter = {
        1: "negative",
        2: "negative",
        3: "neutral",
        4: "positive",
        5: "positive"
    }
    rating["overall"] = rating["overall"].map(converter)


'''
Routine that delete all columns except rating and the review text
'''
def delete_unused_columns(rating: pd.DataFrame):
    rating = rating.drop(columns=["vote", "image", "style", "verified", "reviewTime", "summary",
                                  "unixReviewTime", "reviewerName", "asin", "reviewerID"], axis=1)


'''
Routine that deletes duplicates entries
'''
ratings = pd.DataFrame

ratings = pd.read_json(f'./DataPickles/Movies_and_TV00.json', encoding="ascii", lines=True)
delete_unused_columns(ratings)
convert_star_rating(ratings)

excess_rows_removed = ratings.drop(['verified', 'reviewTime', 'reviewerID', 'asin', 'style', 'reviewerName', 'summary', 'unixReviewTime', 'vote', 'image'], axis=1)

count = 0
for i in excess_rows_removed['reviewText']:
    if i == "":
        count = count + 1
print(f'ReviewText null Count: {count}')

pos, neg = 0, 0
for i in excess_rows_removed['overall']:
    if i == "positive":
        pos += 1
    elif i == "negative":
        neg += 1;

print(f'Overall positive Count: {pos},\nNegative count: {neg}')

lemmatizer = WordNetLemmatizer()
stemmer = EnglishStemmer()

review_text = excess_rows_removed['reviewText']

'''
Removing any white spaces repeating more than once
'''
for text in review_text:
    removed_spaces = re.sub('[ ]+', " ", str(text))

'''
- performing whole pre-processing pipeline which I think is appropriate
stemming is stemming the words as not expected but its overdoing it.
'''
for text in review_text:
    tokenized = word_tokenize(text)
    only_alphas = [re.sub('^[^A-Za-z]+', '', token) for token in tokenized]
    no_spaces = filter(lambda alpha: alpha != '', only_alphas)
    lemmatized = [lemmatizer.lemmatize(token) for token in no_spaces]
    stemmed = [stemmer.stem(token) for token in lemmatized]
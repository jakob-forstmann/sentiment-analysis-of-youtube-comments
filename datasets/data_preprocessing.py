import os
import re
import nltk
import pandas as pd
import numpy as np

from nltk.stem import WordNetLemmatizer
from nltk.stem.snowball import EnglishStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('punkt')
nltk.download('stopwords')

# Just declaring the Number of files variable
NUMBER_OF_FILES = 0
ratings = pd.DataFrame


# Retriving the file names with the help of os module
data_file_names = os.listdir('./DataPickles/')


# write the directory scructure you have for the dataset, and if in the same folder just comment and ignore the below cell
data_file_names = [f'./DataPickles/{file_names}' for file_names in data_file_names]

# Initializing the Number of files variable can be useful later
NUMBER_OF_FILES = len(data_file_names)


# Routine that converts a five star rating into three categories: negative,neutral and positive
def convert_star_rating(rating: pd.DataFrame):
    converter = {
        1: "negative",
        2: "negative",
        3: "neutral",
        4: "positive",
        5: "positive"
    }
    rating["overall"] = rating["overall"].map(converter)

def delete_unused_columns(rating: pd.DataFrame):
    rating = rating.drop(columns=["vote", "image", "style", "verified", "reviewTime", "summary",
                                  "unixReviewTime", "reviewerName", "asin", "reviewerID"], axis=1)

# Routine that deletes duplicates entries
ratings = pd.DataFrame
ratings = pd.read_json(f'./DataPickles/Movies_and_TV00.json', encoding="ascii", lines=True)
delete_unused_columns(ratings)
convert_star_rating(ratings)

rrRatings = ratings.drop(['verified', 'reviewTime', 'reviewerID', 'asin', 'style', 'reviewerName', 'summary', 'unixReviewTime', 'vote', 'image'], axis=1)

count = 0
for i in rrRatings['reviewText']:
    if i == '':
        count = count + 1
print(f'ReviewText null Count: {count}')

pos, neg = 0, 0
for i in rrRatings['overall']:
    if i == "positive":
        pos += 1
    elif i == "negative":
        neg += 1;

print(f'Overall positive Count: {pos},\nNegative count: {neg}')

lemmatizer = WordNetLemmatizer()
stemmer = EnglishStemmer()
english_stopwords = stopwords.words('english')

reviews = rrRatings['reviewText']

preprocessed_reviews = []

for review in reviews:
    review = str(review).lower()
    tokenized = word_tokenize(review)
    no_specials = [re.sub('^[^A-Za-z]+', '', token) for token in tokenized]
    no_blanks = filter(lambda blanks: blanks != "", no_specials)
    no_stopwords = [word for word in no_blanks if word not in english_stopwords]
    lemmatized = [lemmatizer.lemmatize(token) for token in no_stopwords]
#     stemmed = [stemmer.stem(token) for token in lemmatized] Stemming is not what we expected it is overdoing the words.
    preprocessed_reviews.append(' '.join(lemmatized))
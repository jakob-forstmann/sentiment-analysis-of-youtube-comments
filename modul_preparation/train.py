import joblib
import pandas as pd
from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from prepare_training import load_youtube_dataset,load_amazon_dataset

if __name__ =="__main__":   
    youtube_index = load_youtube_dataset()
    youtube_data = youtube_index.load_reviews()
    amazon_revies = load_amazon_dataset()
    comments_train, comments_test, sentiment_train, sentiment_test = train_test_split(
        youtube_data,
        test_size=0.25,
        random_state=42,
    )
    pipeline = Pipeline([('vect', TfidfVectorizer(sublinear_tf=True)), ('clf', LinearSVC())])

    pipeline.fit(youtube_data.loc[:, 'comment'], youtube_data.loc[:, 'sentiment'])
    test_accuracy = pipeline.score(comments_test, sentiment_test)

    joblib.dump(pipeline, './youtube_model.joblib')

    print("Training finished")
    print(f"Final model as test accuracy of {test_accuracy:2%}.")

import joblib
import pandas as pd
from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, cohen_kappa_score, roc_auc_score
from sklearn.model_selection import train_test_split
from .prepare_training import load_comments

def train():
    youtube_index = load_comments()
    youtube_data = youtube_index.load_reviews()
    comments_train, comments_test, sentiment_train, sentiment_test = train_test_split(
        youtube_data.iloc[:, 0],
        youtube_data.iloc[:, 1],
        test_size=0.25,
        random_state=42,
    )
    pipeline = Pipeline([('vect', TfidfVectorizer(sublinear_tf=True)), ('clf', LinearSVC())])

    pipeline.fit(comments_train, sentiment_train)
    test_accuracy = pipeline.score(comments_test, sentiment_test)
    predicted_sentiment = pipeline.predict(comments_test)

    # metrics explained on https://towardsdatascience.com/comprehensive-guide-on-multiclass-classification-metrics-af94cfb83fbd
    metric_results = classification_report(sentiment_test, predicted_sentiment)
    cohen_kappa_result = cohen_kappa_score(sentiment_test, predicted_sentiment)


    joblib.dump(pipeline, './youtube_model.joblib')

    print("Training finished")
    print(f"Final model as test accuracy of {test_accuracy:2%}.")
    print(f"The cohen kappa score is {cohen_kappa_result:.2}.")
    print()
    print(metric_results)

    
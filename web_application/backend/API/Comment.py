import os
import joblib
import json
import pandas as pd

class Comment:
    def __init__(self):
        '''Initialize the trained prediction model'''
        self.prediction_model = joblib.load(os.path.dirname(os.path.realpath(__file__))+"/../resources/TrainedModel/YoutubeModel.joblib")
        # Predicted Comments are to store the comments in pandas
        # dataframe across the class for easy use
        self.predicted_comments = pd.DataFrame(columns=("comment", "sentiment"))

    def get_classified_comments(self, comments):
        '''Predicts all the comments and returns in classified form'''
        predicted_comments = self.predict_comments(comments)
        classified_comments = self.classifying_comments(predicted_comments)
        return json.dumps(classified_comments)

    def predict_comments(self, comments):
        '''Predict the video comments recrived from the client'''
        # Saving the comments from the video
        self.predicted_comments["comment"] = pd.Series(comments)
        # Predicting the Sentiment values of the comments
        self.predicted_comments["sentiment"] = self.prediction_model.predict(self.predicted_comments["comment"])
        return self.predicted_comments

    def classifying_comments(self, comments):
        '''Classifying the comments in negative postive and neutral from the predicted data'''
        classified_comments = {
            "negative": [],
            "positive": [],
            "neutral": [],
        }
        sentiment = self.predicted_comments["sentiment"]
        negative_comments = list(self.predicted_comments[sentiment == "negative"]["comment"])
        positive_comments = list(self.predicted_comments[sentiment == "positive"]["comment"])
        neutral_comments = list(self.predicted_comments[sentiment == "neutral"]["comment"])
        classified_comments["negative"] = negative_comments
        classified_comments["positive"] = positive_comments
        classified_comments["neutral"] = neutral_comments
        return classified_comments

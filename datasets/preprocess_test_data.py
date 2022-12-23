import pandas as pd
import re

raw_test_data = pd.read_csv("data/Youtube Comments - Sheet1.csv").squeeze("columns")

def preprocess_comment(comment):
    # Remove all the special characters
    processed_comment = re.sub(r'\W', ' ', comment)

    # remove all single characters
    processed_comment= re.sub(r'\s+[a-zA-Z]\s+', ' ', processed_comment)

    # Remove single characters from the start
    processed_comment = re.sub(r'^[a-zA-Z]\s+', ' ', processed_comment) 

    # Substituting multiple spaces with single space
    processed_comment = re.sub(r'\s+', ' ', processed_comment, flags=re.I)

    # Removing prefixed 'b'
    processed_comment = re.sub(r'^b\s+', '', processed_comment)

    # Converting to Lowercase
    processed_comment = processed_comment.lower()
    
    return processed_comment

preprocessed_test_data = raw_test_data.apply(preprocess_comment)
preprocessed_test_data.to_csv("data/test_data.csv")


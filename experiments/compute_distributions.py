import pandas as pd
from training_with_Amazon_reviews.dataset_converter import create_dataset,clean_data
from dataset_statistics import temporal_distribution,review_sentiment_distribution,plot_data
from modul_preparation.prepare_training import load_youtube_dataset,load_amazon_dataset,raw_amazon_dataset_path

if __name__ == "__main__":
    youtube_index = load_youtube_dataset()
    youtube_comments = youtube_index.load_reviews()
    amazon_reviews = create_dataset(raw_amazon_dataset_path)
    clean_data(amazon_reviews,keep_review_time=True)
    comments_per_sentiment = review_sentiment_distribution(youtube_comments,col_name="sentiment")
    reviews_per_year = temporal_distribution(amazon_reviews)
    plot_data(reviews_per_year.keys(), reviews_per_year.values(),
                range(2015,2019),
                "../data/reviews_per_sentiment.png")
    plot_data(comments_per_sentiment.keys(), comments_per_sentiment.values(),
                range(2015,2019),
                "../data/comments_per_sentiment.png")
   

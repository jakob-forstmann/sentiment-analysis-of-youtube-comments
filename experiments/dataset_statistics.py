"""
 used to compute the temporal distribution e.g.the number of reviews for each year and 
 the review_sentiment distribution e.g. how many reviews are there per category 
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# index is year from 2015 to 2018,value are all reviews between 1/1 and 31/12 of the same year
reviews_sorted_by_years = [0 for i in range(0,4)]

def temporal_distribution(self, review: pd.DataFrame) -> []:
    """" returns a list with the number of reviews for each year from 2015 to 2018 """
    years_boundary = get_date_boundaries()
    for index, year in enumerate(years_boundary):
        upper_bound = years_boundary[index+1]
        reviews_between_years = review[(
            review["unixReviewTime"] >= year)
            & (review["unixReviewTime"] < upper_bound)]
    reviews_sorted_by_years[index] += reviews_between_years["unixReviewTime"].count()
    return reviews_sorted_by_years

def review_sentiment_distribution(self, review: pd.DataFrame):
    """ calculate the number of reviews for each sentiment
    returns a dict with number of positives,neutral and negatives reviews"""
    reviews_per_sentiment = review["overall"].value_counts().to_dict()
    return reviews_per_sentiment

def get_date_boundaries() -> []:
    """creates a list with the date ranges e.g from 1/1/2015 until 1/1/2016
    returns the values as unix time stamps"""
    years = pd.period_range("1/1/2015", "1/1/2019",
                            freq="y").to_timestamp()
    return convert_to_unix_timestamp(years)

def convert_to_unix_timestamp(years):    
    return  years.astype(np.int64) // 10**9

def plot_data(self, xdata, ydata, name):
    fig = plt.figure()
    fig, ax = plt.subplots()  # figure with one axes
    # plot data on axes
    ax.bar(xdata, ydata)
    plt.show()
    fig.savefig(name)


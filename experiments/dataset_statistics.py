"""
 used to compute the temporal distribution e.g.the number of reviews for each year and 
 the review_sentiment distribution e.g. how many reviews are there per category 
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

years ={0:2015,1:2016,2:2017,3:2018}
reviews_sorted_by_years ={}

def temporal_distribution(review: pd.DataFrame) -> {}:
    """" returns a list with the number of reviews for each year from 2015 to 2018 """
    years_boundary = get_date_boundaries()
    for index, year in enumerate(years_boundary):
        lower_bound =year
        # handle all dates greater than 01/01/2018 e.g the last entry in years_to_consider
        if index == len(years_boundary)-1:
            reviews_between_years = review[
            review["unixReviewTime"] >= lower_bound]
        else:
            upper_bound =years_boundary[index+1]
            reviews_between_years = review[(
                review["unixReviewTime"] >= lower_bound)
                & (review["unixReviewTime"] < upper_bound)]
        current_year_range = years[index]
        reviews_sorted_by_years[current_year_range] = reviews_between_years["unixReviewTime"].count()
    return reviews_sorted_by_years

def review_sentiment_distribution(review: pd.DataFrame,col_name)->pd.Series:
    """ calculate the number of reviews for each sentiment
    returns a dict with number of positives,neutral and negatives reviews"""
    return review[col_name].value_counts().to_dict()

def get_date_boundaries() -> []:
    """creates a list with the date ranges e.g from 1/1/2015 until 1/1/2016
    returns the values as unix time stamps"""
    years = pd.period_range("1/1/2015", "1/1/2018",
                            freq="y").to_timestamp()
    return convert_to_unix_timestamp(years)

def convert_to_unix_timestamp(years):    
    return  years.astype(np.int64) // 10**9

def plot_data(xdata, ydata,x_ticks,name):
    fig = plt.figure()
    fig, ax = plt.subplots()  # figure with one axes
    # plot data on axes
    plt.xticks(x_ticks)
    print(f"xdata{xdata}")
    ax.bar(xdata, ydata)
    fig.savefig(name)


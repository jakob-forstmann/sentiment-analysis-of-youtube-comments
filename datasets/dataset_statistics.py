import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class DatasetStatistics():
    """ computes statistics about the used dataset """

    def __init__(self):
        """ indicies are the years 1996 to 2018,elements are the reviews between the 1/1 of
        the year and the 1/1/ of the next year excluding reviews published on 1/1 of the
        following year"""
        self.reviews_sorted_by_years = [0, 0, 0, 0, 0, 0, 0,
                                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    def temporal_distribution(self, review: pd.DataFrame) -> []:
        """" returns a list with the number of reviews for each year from 1996 to 2018 """
        years_boundary = self.get_date_boundaries()
        for index, year in enumerate(years_boundary):
            lower_boundary_year = year
            # handle all dates greater than 01/01/2018 e.g the last entry in years_to_consider
            if index == len(years_boundary)-1:
                reviews_between_years = review[
                    review["unixReviewTime"] >= lower_boundary_year]
            else:
                upper_boundary_year = years_boundary[index+1]
                reviews_between_years = review[(
                    review["unixReviewTime"] >= lower_boundary_year)
                    & (review["unixReviewTime"] < upper_boundary_year)]
            self.reviews_sorted_by_years[index] += reviews_between_years["unixReviewTime"].count()
        return self.reviews_sorted_by_years

    def number_of_reviews_per_sentiment(self, review: pd.DataFrame):
        """ returns a dict with number of positives,neutral and negatives reviews"""
        reviews_per_sentiment = review["overall"].value_counts().to_dict()
        return reviews_per_sentiment

    def get_date_boundaries(self) -> []:
        """creates a list with the date ranges e.g from 1/1/1996 until 1/1/1997
        returns the values as unix time stamps"""
        years = pd.period_range("1/1/1996", "1/1/2018",
                                freq="y").to_timestamp()
        # convert dates to unix time: np.int64 converts date to
        # unix timestamp in nanoseconds, divide by 10⁹ to get ms
        years_boundary = years.astype(np.int64) // 10**9
        return years_boundary

    def plot_data(self, xdata, ydata, name):
        fig = plt.figure()
        fig, ax = plt.subplots()  # figure with one axes
        # plot data on axes
        ax.bar(xdata, ydata)
        plt.show()
        fig.savefig(name)

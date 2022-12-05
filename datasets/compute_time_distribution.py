import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

NUMBER_OF_SPLITTED_FILES = 9


def get_data():
    data = []
    file_name_prefix = "Movies_and_TV0"
    for i in range(0, NUMBER_OF_SPLITTED_FILES):
        file_name = file_name_prefix+str(i)+".json"
        rating = pd.read_json(file_name, encoding="ascii", lines=True)
        data.append(rating)
    return data


""""
fill the array reviews_sorted_by_year with all reviews between two date ranges """


def get_temporal_distribution(review: pd.DataFrame) -> []:
    years_to_consider = get_date_boundaries()
    for index, year in enumerate(years_to_consider):
        lower_boundary_year = year
        # handle all dates greater than 01/01/2018 e.g the last entry in years_to_consider
        if index == len(years_to_consider)-1:
            reviews_between_date_ranges = review[
                review["unixReviewTime"] >= lower_boundary_year]
        else:
            upper_boundary_year = years_to_consider[index+1]
            reviews_between_date_ranges = review[(
                review["unixReviewTime"] >= lower_boundary_year)
                & (review["unixReviewTime"] < upper_boundary_year)]
        number_reviews = reviews_between_date_ranges["unixReviewTime"].count()
        reviews_sorted_by_years[index] += number_reviews


"""
creates a list with the date ranges e.g from 1/1/1996 until 1/1/1997
returns the values as unix time stamps"""


def get_date_boundaries() -> []:
    years_to_consider = pd.period_range(
        "1/1/1996", "1/1/2018", freq="y").to_timestamp()
    # convert dates to unix time: np.int64 converts date to unix time
    #  in nanoseconds, divide by 10⁹ to get ms
    years_to_consider = years_to_consider.astype(np.int64) // 10**9
    return years_to_consider


def plot_data(xdata, ydata, name):
    fig = plt.figure()  # would be an empty figure without any axes
    fig, ax = plt.subplots()  # figure with one axes
    # plot data on axes
    ax.bar(xdata, ydata)
    plt.show()
    fig.savefig(name)


# reviews_sorted_by_year[0] are f.ex. all reviews between 1/1/1996 and 1/1/1997 excluding reviews published on 1/1/1997
reviews_sorted_by_years = [0, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
reviews = get_data()
for review in reviews:
    get_temporal_distribution(review)

years = [1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006,
         2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018]

plot_data(years, reviews_sorted_by_years, "reviews_full_plot")
reviews_from_1996_to_2010 = reviews_sorted_by_years[0:15]
years_from_1996_to_2010 = years[0:15]
plot_data(years_from_1996_to_2010, reviews_from_1996_to_2010,
          "reviews_from_1996_to_2004")

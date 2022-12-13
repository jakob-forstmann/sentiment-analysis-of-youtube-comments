import random
import pandas as pd
from dataset_statistics import DataSet


class DatasetSampling:
    """splits the dataset into a smaller dataset using relevance sampling """

    def __init__(self, reviews_to_use_for_distribution: [{}], distribution="equally"):
        """ specify if you want to distribute the reviews equally or not, see below.
        all_reviews: a list of dataframes for each splitted file
        distribution:
        if set to equally, the number of positve,neutral and negatives reviews
        will be equal in the new dataset.Note that this is not the case in the original dataset.
        if set to keep the distribution of positive,negative and neutral reviews of the original
        file will be almost the same in the smaller dataset.

        reviews_to_use_for_distribution: a list of dicts
        if distribution is set to equally: a list with one dict containing the positive,negative
        and neutral reviews to include in the smaller dataset

        if distribution is set to keep:
        a list of dicts where each dict has the number of positives,
        neutral and negatives reviews for the file with the number of the index+1.
        f.ex. the second entry contains a dict the number of positives,neutrals and negatives
        reviews for the third file.
        """

        self.handle_distribution = {"equally": self.distribute_reviews_equally,
                                    "keep": self.keep_old_distribution,
                                    }
        self.can_distribute = self.handle_distribution[distribution]

        self.included_sentiments = {
            "positive": 0, "neutral": 0, "negative": 0}
        self.reviews_to_use_for_distribution = reviews_to_use_for_distribution
        self.possible_reviews_nums = list(range(0, DataSet.reviews_per_file))

    def get_number_reviews_per_file(self, new_number_of_reviews):
        # TODO: handle case when new_number_of_reviews is not
        # divisable by the number of lines in the huge dataset
        reviews_to_include_per_file = new_number_of_reviews // DataSet.number_of_splitted_files
        if reviews_to_include_per_file == 0:
            reviews_to_include_per_file = 1
        return reviews_to_include_per_file

    def split_dataset(self, new_number_of_reviews, all_reviews: []):
        """ split the dataframe with all reviews to a smaller dataframe which has
        number_of_reviews reviews with the distribution specified at creation
        TODO: maybe also consider the number of reviews per year when splitting the dataset
        """
        reviews_for_smaller_dataset = []
        already_included_reviews = 0
        max_reviews = self.get_number_reviews_per_file(new_number_of_reviews)
        for file_number, reviews_in_file in enumerate(all_reviews):
            while already_included_reviews < max_reviews:
                review = self.select_review_from_file(reviews_in_file)
                if self.can_distribute(review, file_number):
                    already_included_reviews += 1
                    reviews_for_smaller_dataset.append(review)
        return pd.DataFrame(reviews_for_smaller_dataset)

    def select_review_from_file(self, reviews_in_file):
        review_number = random.randrange(len(self.possible_reviews_nums))
        self.possible_reviews_nums.pop(review_number)
        return reviews_in_file.loc[review_number]

    def keep_old_distribution(self, review, file_number):
        current_sentiment = review["overall"]
        reviews_per_sentiment_to_use = self.reviews_to_use_for_distribution[file_number]
        return self.can_add_review_to_distribution(current_sentiment, reviews_per_sentiment_to_use)

    def distribute_reviews_equally(self, review, file_number):
        current_sentiment = review["overall"]
        reviews_per_sentiment_to_use = self.reviews_to_use_for_distribution[0]
        return self.can_add_review_to_distribution(current_sentiment, reviews_per_sentiment_to_use)

    def can_add_review_to_distribution(self, sentiment, reviews_per_sentiment_to_use):
        """ returns True if reviews can be added to smaller dataset
        so that the choosen distribution is kept,otherwise it returns False """
        if self.included_sentiments[sentiment] <= reviews_per_sentiment_to_use[sentiment]:
            self.included_sentiments[sentiment] += 1
            return True
        return False

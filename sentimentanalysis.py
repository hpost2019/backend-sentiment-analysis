import matplotlib.pyplot as plt
import numpy as np
from gathertweets import get_tweets


def find_negative_tweets(test_tweets):
    """Function returns all negative Tweets"""
    return [tweet for tweet in test_tweets
            if tweet['sentiment'] == 'negative']


def find_positve_tweets(test_tweets):
    """Function returns all negative Tweets"""
    return [tweet for tweet in test_tweets
            if tweet['sentiment'] == 'positive']


def plot_response(negative, positive, term):
    """Function to create bar graph for response"""
    title = 'Sentiment Analysis for ' + term
    label = ('Positive', 'Negative')
    sentiment = [positive, negative]
    index = np.arange(len(label))
    plt.barh(index, sentiment, align='center')
    plt.xlabel('Percentage', fontsize=5)
    plt.ylabel('Sentiment', fontsize=5)
    plt.yticks(index, label, fontsize=5)
    plt.title(title)
    plt.show()


def main():
    search_list = []
    search_term = input("Enter the topic you want to search for: ")
    search_list.append(search_term)
    test_tweets = get_tweets(search_list)
    num_tweets = len(test_tweets)
    neg_tweets = len(find_negative_tweets(test_tweets))
    pos_tweets = len(find_positve_tweets(test_tweets))
    neutral = num_tweets - neg_tweets - pos_tweets
    num_tweets = num_tweets - neutral
    neg_percent = (100*neg_tweets/num_tweets)
    pos_percent = (100*pos_tweets/num_tweets)
    print("**** RESULTS ****")
    print("Total Tweets Captured: ", len(test_tweets))
    print("Neutral Tweets: ", neutral)
    print("Positive Tweets: ", pos_tweets)
    print("Negative Tweets: ", neg_tweets)
    print("DISCLAIMER: Graph does not display Neutral Tweets")
    plot_response(neg_percent, pos_percent, search_list[0])
    pass


if __name__ == '__main__':
    main()

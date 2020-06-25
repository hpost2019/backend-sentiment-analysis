import tweepy
from dotenv import load_dotenv
import os
import csv
import re
from string import punctuation
from textblob import TextBlob

load_dotenv()


auth = tweepy.OAuthHandler(os.environ['CONSUMER_KEY'],
                           os.environ['CONSUMER_SECRET'])
auth.set_access_token(os.environ['ACCESS_KEY'], os.environ['ACCESS_SECRET'])

api = tweepy.API(auth)

tweets = []


class MyStreamListner(tweepy.StreamListener):
    tweet_counter = 1

    def __init__(self):
        """Class Initializer. Strips Tweets of
        puntuation, and AT_USER, URL inside tweet"""
        super(MyStreamListner, self).__init__()
        # self.auth = tweepy.OAuthHandler(os.environ['CONSUMER_KEY'],
        #                                 os.environ['CONSUMER_SECRET'])
        # self.set_access_token(os.environ['ACCESS_KEY'],
        #                       os.environ['ACCESS_SECRET'])
        # self.api = tweepy.API(self.auth)
        self._strip_tweet = list(punctuation) + ['AT_USER', 'URL']

    def clean_tweet(self, tweet):
        """Cleans tweet using regex to replace URLs with word URL,
        usernames with AT_USER, gets rid of hashtag on tweets"""
        tweet = tweet.lower()
        tweet = re.sub(r'((www\.[^\s]+)|(https?://[^\s]+))', 'URL', tweet)
        tweet = re.sub(r'@[^\s]+', 'AT_USER', tweet)
        tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
        return tweet

    def get_sentiment(self, tweet):
        """Using textblob's sentiment method this function classifies
        sentiment of passed in tweet"""
        analysis = TextBlob(self.clean_tweet(tweet))
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def on_status(self, status):
        try:
            MyStreamListner.tweet_counter += 1
            tweet_obj = status
            if 'extended_tweet' in tweet_obj._json:
                tweet = tweet_obj.extended_tweet['full_text']
            else:
                tweet = tweet_obj.text

            '''Replaces all named and numeric character
            references with Unicode characters'''
            tweet = (tweet.replace('&amp;', '&')
                     .replace('&lt;', '<')
                     .replace('&gt;', '>')
                     .replace('&quot;', '"')
                     .replace('&#39;', "'")
                     .replace(';', " ")
                     .replace(r'\u', " "))
            # print(tweet)
            tweet_dict = {}
            tweet_dict['text'] = tweet
            tweet_dict['sentiment'] = self.get_sentiment(tweet)
            # Checks if tweet and been retweeted, if so it will
            # only add it once.
            if tweet_obj.retweet_count > 0:
                if tweet_dict not in tweets:
                    tweets.append(tweet_dict.copy())
            else:
                tweets.append(tweet_dict.copy())
            if MyStreamListner.tweet_counter < 201:
                print('Captured Tweet number:', MyStreamListner.tweet_counter)
                return True
            else:
                return False
        except Exception as e:
            print('Encountered problem:', e)
            pass


def get_tweets(terms):
    streamingAPI = tweepy.streaming.Stream(auth, MyStreamListner())
    streamingAPI.filter(track=terms)

    return tweets

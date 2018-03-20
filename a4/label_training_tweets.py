import glob
import nltk
import re
from textblob import TextBlob


def read_tweets(filename):
    f = open(filename, "r")
    tweets = f.read().splitlines()
    f.close()
    return tweets


def main():

    tweets = read_tweets('training_tweets.txt')
    sentiment_tweets = []
    tokens = []
    tokenize_sentiment = []
    f = open("labelled_tweets.txt", 'w')

    for tweet in tweets:
        print(tweet)
        sentiment = input("Is this tweet pos, neg or neutral: \n")
        f.write(tweet+'\n')
        f.write(sentiment+'\n')


if __name__ == '__main__':
    main()

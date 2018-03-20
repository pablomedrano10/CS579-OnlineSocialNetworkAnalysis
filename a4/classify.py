import glob
import nltk
import re


def read_tweets(filename):
    tokens = []
    tweet = []
    training_tweets = []
    f = open(filename, "r")
    tweets = f.read().splitlines()
    f.close()
    for line in tweets:
        tweet = re.sub('\W+', ' ', line).split()
        for item in tweet:
            tokens = []
            for i in range(0, len(tweet)-2):
                tokens.append(tweet[i])
        training_tweets.append((tokens, tweet[len(tweet)-1]))

    return training_tweets

def read_training_tweets(filename):
    training_tweets = []
    tweet = []
    f = open(filename, "r")
    tweets = f.read().splitlines()
    for i in range(0, len(tweets)-1, 2):
        training_tweets.append([{word: True for word in nltk.word_tokenize(tweets[i])}, tweets[i+1]])

    return training_tweets

def read_test_tweets(filename):
    test_tweets = []
    tweet = []
    f = open(filename, "r")
    tweets = f.read().splitlines()
    for tweet in tweets:
        test_tweets.append({word: True for word in nltk.word_tokenize(tweet)})

    return test_tweets


def main():

    training_tweets = read_training_tweets('labelled_tweets.txt')
    print(training_tweets)
    test_tweets = read_test_tweets('test_tweets.txt')
    classifier = nltk.NaiveBayesClassifier.train(training_tweets)

    num_of_pos = 0
    num_of_neutral = 0
    num_of_neg = 0

    for tweet in test_tweets:
        keys = []
        for key in tweet:
            keys.append(key)
        print("This tweet ", keys, " is: ", classifier.classify(tweet))
        if classifier.classify(tweet) == 'pos':
            num_of_pos += 1
            positive_tweet = tweet
        elif classifier.classify(tweet) == 'neg':
            num_of_neg += 1
            negative_tweet = tweet
        elif classifier.classify(tweet) == 'neutral':
            num_of_neutral += 1
            neutral_tweet = tweet

    pos_tweet = []
    for key in positive_tweet.keys():
        pos_tweet.append(str(key))

    neg_tweet = []
    for key in negative_tweet.keys():
        neg_tweet.append(str(key))

    neut_tweet = []
    for key in neutral_tweet.keys():
        neut_tweet.append(str(key))

    f = open("classify_results.txt", 'w')
    f.write("number of positives instances:"+str(num_of_pos)+'\n')
    f.write("number of negatives instances:"+str(num_of_neg)+'\n')
    f.write("number of neutral instances:"+str(num_of_neutral)+'\n')
    f.write("This is a positive tweet:"+str(pos_tweet)+'\n')
    f.write("This is a negative tweet:"+str(neg_tweet)+'\n')
    f.write("This is a neutral tweet:"+str(neut_tweet)+'\n')
    f.close()



if __name__ == '__main__':
    main()

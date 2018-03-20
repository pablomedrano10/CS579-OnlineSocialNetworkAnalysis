import os
from TwitterAPI import TwitterAPI
import re

consumer_key = '7wQkcnWkYSWhy54KhIjenzila'
consumer_secret = 'OxJGwlHQRdm9AMtrUteoBtQrXVGv1ZApAAqbMb8Sx0dVK7xJgS'
access_token = '459979519-2VifLRNGfZaLZry0QYAD5FVWBYvjXnjtTIS8s7GR'
access_token_secret = 'ZS2gObLq6VDRgs8MNlDOxHJTnC1o4XQI62F3t9n4wpHRd'

def get_twitter():
    """ Construct an instance of TwitterAPI using the tokens you entered above.
    Returns:
      An instance of TwitterAPI.
    """
    return TwitterAPI(consumer_key, consumer_secret, access_token, access_token_secret)

def collect_tweets(twitter, n):
    # Collect n tweets.
    tweets = []
    while True:
        r = twitter.request('statuses/filter', {'track':'football', 'language':'en'})
        if r.status_code != 200: # error
            break
        else:
            for item in r.get_iterator():
                tweets.append(item)
                if len(tweets) >= n:
                    break
                elif len(tweets) % 100 == 0:
                    print(len(tweets))


    tweets = [t for t in tweets if 'text' in t]
    print(len(tweets))
    return tweets

def tokenize(string, lowercase, keep_punctuation, prefix,
             collapse_urls, collapse_mentions):
    """ Split a tweet into tokens."""
    if not string:
        return []
    if lowercase:
        string = string.lower()
    tokens = []
    if collapse_urls:
        string = re.sub('http\S+', '', string)
    if collapse_mentions:
        string = re.sub('@\S+', '', string)
    if keep_punctuation:
        tokens = string.split()
    else:
        tokens = re.sub('\W+', ' ', string)
    if prefix:
        tokens = ['%s%s' % (prefix, t) for t in tokens]
    return tokens

def save_screen_names(tweets):
    f = open("ids.txt", 'w')

    ids = [tweet['user']['id'] for tweet in tweets]
    for ID in ids:
        f.write(str(ID)+'\n')
    f.close()

    return

def save_test_tweets(tweets):
    f = open("test_tweets.txt", 'w')

    tokens = []

    for tweet in tweets:
        tokens.append(tokenize(tweet['text'], lowercase=True, keep_punctuation=False, prefix = False, collapse_urls=True, collapse_mentions=True))

    for token in tokens:
        f.write(str(token)+'\n')
    f.close()

    return

def save_training_tweets(tweets):
    f = open("training_tweets2.txt", 'w')

    tokens = []

    for tweet in tweets:
        tokens.append(tokenize(tweet['text'], lowercase=True, keep_punctuation=False, prefix = False, collapse_urls=True, collapse_mentions=True))

    for token in tokens:
        f.write(str(token)+'\n')
    f.close()

    return


def main():

    twitter = get_twitter()
    tweets = collect_tweets(twitter, 300)
    save_training_tweets(tweets[0:199])
    save_test_tweets(tweets[200:299])
    save_screen_names(tweets[200:299])


if __name__ == '__main__':
    main()

# coding: utf-8

# # Assignment 3:  Recommendation systems
#
# Here we'll implement a content-based recommendation algorithm.
# It will use the list of genres for a movie as the content.
# The data come from the MovieLens project: http://grouplens.org/datasets/movielens/

# Please only use these imports.
from collections import Counter, defaultdict
import math
import numpy as np
import os
import pandas as pd
import re
from scipy.sparse import csr_matrix
import urllib.request
import zipfile

def download_data():
    """ DONE. Download and unzip data.
    """
    url = 'https://www.dropbox.com/s/h9ubx22ftdkyvd5/ml-latest-small.zip?dl=1'
    urllib.request.urlretrieve(url, 'ml-latest-small.zip')
    zfile = zipfile.ZipFile('ml-latest-small.zip')
    zfile.extractall()
    zfile.close()


def tokenize_string(my_string):
    """ DONE. You should use this in your tokenize function.
    """
    return re.findall('[\w\-]+', my_string.lower())


def tokenize(movies):
    """
    Append a new column to the movies DataFrame with header 'tokens'.
    This will contain a list of strings, one per token, extracted
    from the 'genre' field of each movie. Use the tokenize_string method above.

    Note: you may modify the movies parameter directly; no need to make
    a new copy.
    Params:
      movies...The movies DataFrame
    Returns:
      The movies DataFrame, augmented to include a new column called 'tokens'.

    >>> movies = pd.DataFrame([[123, 'Horror|Romance'], [456, 'Sci-Fi']], columns=['movieId', 'genres'])
    >>> movies = tokenize(movies)
    >>> movies['tokens'].tolist()
    [['horror', 'romance'], ['sci-fi']]
    """
    ###TODO
    genres = movies['genres'].tolist()
    tokens = []
    for genre in genres:
        tokens.append(tokenize_string(genre))
    movies['tokens'] = pd.Series(tokens)
    return movies


def featurize(movies):
    """
    Append a new column to the movies DataFrame with header 'features'.
    Each row will contain a csr_matrix of shape (1, num_features). Each
    entry in this matrix will contain the tf-idf value of the term, as
    defined in class:
    tfidf(i, d) := tf(i, d) / max_k tf(k, d) * log10(N/df(i))
    where:
    i is a term
    d is a document (movie)
    tf(i, d) is the frequency of term i in document d
    max_k tf(k, d) is the maximum frequency of any term in document d
    N is the number of documents (movies)
    df(i) is the number of unique documents containing term i

    Params:
      movies...The movies DataFrame
    Returns:
      A tuple containing:
      - The movies DataFrame, which has been modified to include a column named 'features'.
      - The vocab, a dict from term to int. Make sure the vocab is sorted alphabetically as in a2 (e.g., {'aardvark': 0, 'boy': 1, ...})
    """
    ###TODO
    freqs = defaultdict(int)
    vocab = defaultdict(int)
    df = defaultdict(int)
    tokens = movies['tokens'].tolist()
    token_list = []
    freqs_per_movie = defaultdict(int)
    freqs_per_movie_list = []
    vals = []
    cols = []
    matrices = []
    rows = []

    N = movies.shape[0]

    for item in tokens:
        freqs_per_movie.clear()
        for token in item:
            freqs_per_movie[token] += 1
            if token not in token_list:
                token_list.append(token)
        freqs_per_movie_list.append(sorted(freqs_per_movie.items(), key = lambda x: x[1]))
    token_list.sort()

    for i in range(0, len(token_list)):
        vocab[token_list[i]] = i

    for token in token_list:
        for item in tokens:
            if token in item:
                df[token] += 1
    for i in range(0, len(freqs_per_movie_list)):
        for token in freqs_per_movie_list[i]:
            del vals[:]
            del cols[:]
            del rows[:]
            vals.append((token[1]/(freqs_per_movie_list[i][0][1]) * (math.log10(N/df[token[0]]))))
            ind = vocab[token[0]]
            cols.append(ind)
            rows.append(0)
            csr = csr_matrix((vals, (rows, cols)), shape = (1, len(vocab)))
            matrices.append(csr)
    movies['features'] = pd.Series(matrices)
    return movies, vocab




def train_test_split(ratings):
    """DONE.
    Returns a random split of the ratings matrix into a training and testing set.
    """
    test = set(range(len(ratings))[::1000])
    train = sorted(set(range(len(ratings))) - test)
    test = sorted(test)
    return ratings.iloc[train], ratings.iloc[test]


def cosine_sim(a, b):
    """
    Compute the cosine similarity between two 1-d csr_matrices.
    Each matrix represents the tf-idf feature vector of a movie.
    Params:
      a...A csr_matrix with shape (1, number_features)
      b...A csr_matrix with shape (1, number_features)
    Returns:
      The cosine similarity, defined as: dot(a, b) / ||a|| * ||b||
      where ||a|| indicates the Euclidean norm (aka L2 norm) of vector a.
    """
    ###TODO
    arr_a = a.toarray()
    arr_b = b.toarray()
    num = 0
    den = 0

    num = np.dot(arr_a, arr_b.T)
    normA = np.linalg.norm(arr_a, ord = 2)
    normB = np.linalg.norm(arr_b, ord = 2)
    den = normA*normB

    cos = num/den

    return (cos)


def make_predictions(movies, ratings_train, ratings_test):
    """
    Using the ratings in ratings_train, predict the ratings for each
    row in ratings_test.

    To predict the rating of user u for movie i: Compute the weighted average
    rating for every other movie that u has rated.  Restrict this weighted
    average to movies that have a positive cosine similarity with movie
    i. The weight for movie m corresponds to the cosine similarity between m
    and i.

    If there are no other movies with positive cosine similarity to use in the
    prediction, use the mean rating of the target user in ratings_train as the
    prediction.

    Params:
      movies..........The movies DataFrame.
      ratings_train...The subset of ratings used for making predictions. These are the "historical" data.
      ratings_test....The subset of ratings that need to predicted. These are the "future" data.
    Returns:
      A numpy array containing one predicted rating for each element of ratings_test.
    """
    ###TODO
    num = 0
    den = 0
    matrices = movies['features'].tolist()
    predictions = []

    for index, row in ratings_test.iterrows():
        csr_val = movies.loc[movies['movieId'] == row['movieId']]['movieId'].index
        csr_matrix = matrices[csr_val[0]-1]
        rating_user = ratings_train.loc[ratings_train['userId'] == row['userId']]
        for index, row2 in rating_user.iterrows():
            csr2_val = movies.loc[movies['movieId'] == row2['movieId']]['movieId'].index
            csr2_matrix = matrices[csr2_val[0]-1]
            cos = cosine_sim(csr_matrix, csr2_matrix)
            if cos > 0:
                num += row2['rating']*cos
                den += cos
        predict = num/den
        predictions.append(predict)

    return (predictions)

def mean_absolute_error(predictions, ratings_test):
    """DONE.
    Return the mean absolute error of the predictions.
    """
    return np.abs(predictions - np.array(ratings_test.rating)).mean()


def main():
    download_data()
    path = 'ml-latest-small'
    ratings = pd.read_csv(path + os.path.sep + 'ratings.csv')
    movies = pd.read_csv(path + os.path.sep + 'movies.csv')
    movies = tokenize(movies)
    movies, vocab = featurize(movies)
    print('vocab:')
    print(sorted(vocab.items())[:10])
    ratings_train, ratings_test = train_test_split(ratings)
    print('%d training ratings; %d testing ratings' % (len(ratings_train), len(ratings_test)))
    predictions = make_predictions(movies, ratings_train, ratings_test)
    print('error=%f' % mean_absolute_error(predictions, ratings_test))
    print(predictions[:10])


if __name__ == '__main__':
    main()

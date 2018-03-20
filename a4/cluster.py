import sys
import time
import os
from TwitterAPI import TwitterAPI
import re
import warnings
warnings.filterwarnings("ignore")
import matplotlib.pyplot as plt
import itertools
from networkx.algorithms.community.centrality import girvan_newman
import networkx as nx


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

def robust_request(twitter, resource, params, max_tries=5):
    """ If a Twitter request fails, sleep for 15 minutes.
    Do this at most max_tries times before quitting.
    Args:
      twitter .... A TwitterAPI object.
      resource ... A resource string to request; e.g., "friends/ids"
      params ..... A parameter dict for the request, e.g., to specify
                   parameters like screen_name or count.
      max_tries .. The maximum number of tries to attempt.
    Returns:
      A TwitterResponse object, or None if failed.
    """
    for i in range(max_tries):
        request = twitter.request(resource, params)
        if request.status_code == 200:
            return request
        else:
            print('Got error %s \nsleeping for 15 minutes.' % request.text)
            sys.stderr.flush()
            time.sleep(61 * 15)


def read_ids(filename):
    """
    Read a text file containing Twitter screen_names, one per line.
    Params:
        filename....Name of the file to read.
    """
    ###TODO
    ids = []
    my_file = open(filename, "r")
    lines = my_file.read().splitlines()
    my_file.close()
    for line in lines:
        ids.append(int(line))
    return ids


def get_friends(twitter, ID):
    """ Return a list of Twitter IDs for users that this person follows, up to 5000.
    See https://dev.twitter.com/rest/reference/get/friends/ids
    Note, because of rate limits, it's best to test this method for one candidate before trying
    on all candidates.
    Args:
        twitter.......The TwitterAPI object
        screen_name... a string of a Twitter screen name
    Returns:
        A list of ints, one per friend ID, sorted in ascending order.
    Note: If a user follows more than 5000 accounts, we will limit ourselves to
    the first 5000 accounts returned.
    In this test case, I return the first 5 accounts that I follow.
    >>> twitter = get_twitter()
    >>> get_friends(twitter, 'aronwc')[:5]
    [695023, 1697081, 8381682, 10204352, 11669522]
    """
    ###TODO
    ids=[]
    request = robust_request(twitter, 'friends/ids', {'user_id': ID, 'count':500}, 1000)
    ids = [item for item in request]
    ids.sort(key = int)
    return ids

def create_graph(ids, friends):
    graph = nx.DiGraph()
    for i in range(0, 5):
        graph.add_node(ids[i])
        for item in friends:
            for ID in item:
                if ID in friends[i]:
                    graph.add_edge(ID, ids[i])
    return graph


def main():
    """ Main method. You should not modify this. """
    twitter = get_twitter()
    ids = read_ids('ids.txt')
    friends = []
    for i in range(0, 5):
        friends.append(get_friends(twitter, ids[i]))

    ids_int = []
    for ID in ids:
        ids_int.append(int(ID))
    graph = create_graph(ids, friends)

    k = 10
    comp = girvan_newman(graph)
    result =[[len(c) for c in communities]  for communities in itertools.islice(comp, k)][9]
    print(result)
    average_users = 0
    for i in result:
        average_users += i
    average_users = average_users/k

    f = open("cluster_results.txt", 'w')
    f.write("number of communities discovered: "+str(k)+'\n')
    f.write("average number of users per community: "+str(average_users)+'\n')
    f.close()


if __name__ == '__main__':
    main()

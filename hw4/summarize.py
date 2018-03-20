import re
import glob

def get_number_users(filename):
    f = open(filename, 'r')
    screen_names = f.read().splitlines()
    f.close()

    return len(screen_names)

def get_number_tweets(filename):
    f = open(filename, 'r')
    tweets = f.read().splitlines()
    f.close()

    return(len(tweets))

def get_classify_info(filename):
    f = open("classify_results.txt", 'r')
    classify_results = f.read().splitlines()
    f.close()

    return classify_results

def get_cluster_info(filename):
    f = open("cluster_results.txt", 'r')
    cluster_results = f.read().splitlines()
    f.close()

    return cluster_results

def main():

    number_users = get_number_users("ids.txt")
    number_training_tweets = get_number_tweets("training_tweets.txt")
    number_test_tweets = get_number_tweets("test_tweets.txt")
    classify_info = get_classify_info("classify_results.txt")
    cluster_info = get_cluster_info("cluster_results.txt")

    f = open("summary.txt", 'w')
    f.write("number of users collected: "+str(number_users)+'\n')
    f.write("number of training tweets collected: "+str(number_training_tweets)+'\n')
    f.write("number of test tweets collected: "+str(number_test_tweets)+'\n')
    for i in range (0, len(classify_info)):
        f.write(str(classify_info[i])+'\n')
    for i in range (0, len(cluster_info)):
        f.write(str(cluster_info[i])+'\n')
    f.close()



if __name__ == '__main__':
    main()

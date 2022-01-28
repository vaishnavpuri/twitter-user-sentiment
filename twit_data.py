import os
from turtle import Screen
import tweepy as tp
import pandas as pd
import numpy as np
import time
import string
from twit_api import *
from datetime import datetime
from dotenv import load_dotenv


#make directory if one doesnt exist for the date, otherwise do nothing if exists
def mk_dir(path,date):
    exists = os.path.exists(path + date)

    if not exists:
        os.makedirs(path + date)
        print("new directory made")

#get latest tweets (about 3000) associated to a twitter name , get tweet id, create and store in a df
# then save in a csv file
def get_all_tweets(screen_name, api=api, today = today):
    #init list to hold tweets
    allTweets= []

    #request recent tweets, 200 at most
    new_tweets= api.user_timeline(screen_name = screen_name, count=200)
    #save recent tweets
    allTweets.extend(new_tweets)
    #save id of oldest tweet less one
    oldest = allTweets[-1].id - 1
    #keep grabbing until no more
    while len(new_tweets) > 0:
        print(f"getting tweets before {oldest}")
        #prevent duplicates
        new_tweets = api.user_timeline(screen_name = screen_name, count=200, max_id=oldest)
        allTweets.extend(new_tweets)
        oldest = allTweets[-1].id -1
        print(f"...{len(allTweets)} tweets downloaded so far")
    #transform tweets into 2d array to go into csv
    outTweets = [
        [
           t.author.name, t.id_str, t.created_at, t.text, t.entities.get('hashtags'), t.author.location,
            t.author.created_at, t.author.url, t.author.screen_name, t.favorite_count, t.favorited,
            t.retweet_count, t.retweeted, t.author.followers_count, t.author.friends_count
        ] for t in allTweets
    ]
    #write csv
    cols = [
        'author_name', 'tweet_id', 'tweet_created_at', 'content', 'hashtags', 'location',
        'author_created_at', 'author_url', 'author_screen_name', 'tweet_favourite_count', 'tweet_favourited', 
        'retweet_count', 'retweeted', 'author_followers_count', 'author_friends_count'
    ]
    df = pd.DataFrame(outTweets, columns = cols)
    mk_dir(path = './data/', date = today)
    df.to_csv('./data/{}/{}_tweets_{}.csv'.format(today, screen_name, today), index = False)
    time.sleep(10)
    return df
#this will see if todays data has been scraped. If yes: read all. If no: drop dpunlicates 
def read_tweet_data(path):
    #get non hidden subdirectories
    sub_dir = [d for d in os.listdir(path) if d[0] != '.']

    #read csv from sub dirs and concatnate 
    files = []
    for d in sub_dir:
        for p in os.listdir(path +d):
            if p[0] != '.':
                files.append(path + d + '/' + p)
    read_csv = []
    for file in files:
        read_csv.append(pd.read_csv(file, converters={'hastags': eval}, encoding='utf-8-sig'))

    read_csv = pd.concat(read_csv)
    tweets_df = read_csv.drop_duplicates(subset = ['tweet_id', 'tweet_created_at'])
    return tweets_df

#handles im scraping
handles = 'elonmusk'

if today not in os.listdir('./data/'):
    for user in handles:
        print(user)
        _= get_all_tweets(user)

tweets_df = read_tweet_data(
    path = './data/'
)
print(tweets_df.shape)


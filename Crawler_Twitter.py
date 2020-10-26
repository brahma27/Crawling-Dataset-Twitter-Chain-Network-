
import tweepy
import pandas as pd
import numpy as np
import csv

# Masukan API Twitter Developer Premium
consumer_key = " " 
consumer_secret = " " 
access_token = " " 
access_token_secret = " " 

auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
auth.set_access_token(access_token, access_token_secret) 
api = tweepy.API(auth,wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

tweets = tweepy.Cursor(api.search_30_day,
                    environment_name='dev',
                    query="from:afrkml Covid-19").items()
pilihan = open('dataset.csv', 'w',encoding="utf-8")
jaw = csv.writer(pilihan, lineterminator='\n')
jaw.writerow(['count', 'tweet','from','to'])
j=0
tweetID_list = []
for tweet in tweets:
    tweet_id = tweet.id_str
    tweetID_list.append(tweet_id)

rep_tweets = tweepy.Cursor(api.search_30_day,
                        environment_name='dev',
                        query='to:afrkml').items(200)

count = 0
folls_list = []
for rep in rep_tweets:
    for twu in tweetID_list:
        if rep.in_reply_to_status_id_str == twu:
            jaw.writerow([count, rep.text, rep.user.screen_name, rep.in_reply_to_screen_name])
            folls_list.append(rep.user.screen_name)
            count += 1

max_search = 0
id_list = []
while max_search<5:
    for f in folls_list:
        q = 'to:'+f
        rep_folls = tweepy.Cursor(api.search_30_day,
                                environment_name='dev',
                                query=q).items(200)
        for rep in rep_folls:
            if rep.id_str not in id_list:
                jaw.writerow([count, rep.text, rep.user.screen_name, rep.in_reply_to_screen_name])
                folls_list.append(rep.user.screen_name)
                id_list.append(rep.id_str)
                count += 1

        max_search += 1
        folls_list = []


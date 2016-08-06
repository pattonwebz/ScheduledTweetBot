#!/usr/bin/env python
# twitterfunctions.py
# description: This file contains all the functions that are used when connecting to Twitter. Almost all of them rely on Tweepy
# copyrigtht: 2015 William Patton - PattonWebz
# licence: GPLv3

import tweepy

def authenticatetwitter(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET):
    # Authenticate with Twitter using keys and secrets and return
    # an 'api' object

    # Authorize with consumer credentials and get an access token
    # with access credentials
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

    # get an authenticated instance of the API class
    api = tweepy.API(auth)

    # return API object 'api'
    return api


def sendtweet(api, tweet):
    # Send 'tweet' using Tweepy API function
    api.update_status(status=tweet)

def sendretweet(api, tweet):
    # Send a retweet - 'tweet' content will be a tweet Id
    api.retweet(tweet)

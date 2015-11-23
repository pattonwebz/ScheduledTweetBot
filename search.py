#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Scheduled Tweet Bot written in Python intended to run on a Raspberry Pi
# (will work anywhere Python and the dependancies are installed though)
# version: 0.9
import tweepy, sys
import dbconnect
import twitterfunctions
from configuration import dbconfig

getKeySecretQuery = ("SELECT CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET FROM Accounts WHERE user = 'default'")

authcnx=dbconnect.dbconnect(dbconfig)
authcursor=dbconnect.dbcursor(authcnx)

gotKeySecretResult = authcursor.execute(getKeySecretQuery)
KeySecretResult = authcursor.fetchall()

for (CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET) in KeySecretResult :
    THE_CONSUMER_KEY = CONSUMER_KEY
    THE_CONSUMER_SECRET = CONSUMER_SECRET
    THE_ACCESS_KEY = ACCESS_KEY
    THE_ACCESS_SECRET = ACCESS_SECRET

api = twitterfunctions.authenticatetwitter(THE_CONSUMER_KEY, THE_CONSUMER_SECRET, THE_ACCESS_KEY, THE_ACCESS_SECRET)


def searchtweets(query, getcount):
    results = api.search(q=query,rpp=1,count=getcount)

    cnx = dbconnect.dbconnect(dbconfig)
    cursor = dbconnect.dbcursor(cnx)

    for result in results:

        tweet = result.text.encode('utf-8')
        user = result.user.screen_name.encode('utf-8')
        timesent = result.created_at
        tweetid = result.id_str.encode('utf-8')

        insertQuery = ('INSERT IGNORE INTO SearchedForTweets '
             '(tweetid, username, tweetcontent, timesent, searchterm) '
             'VALUES '
             '("%s", "%s", %r, "%s", "%s")' % (tweetid, user, tweet, timesent, query))

        cursor.execute(insertQuery)
        cnx.commit()

        print user + " " + tweet


query = str(sys.argv[1])
getcount = int(sys.argv[2])

searchtweets(query, getcount)

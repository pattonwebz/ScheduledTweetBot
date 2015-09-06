#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Scheduled Tweet Bot written in Python intended to run on a Raspberry Pi
# (will work anywhere Python and the dependancies are installed though)
# version: 0.9
import tweepy, time, sys
import dbconnect
import datetime

## set some colors to use in the command line, borrowed from blender build script
## found in this answere here: http://stackoverflow.com/a/287944/2375493
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

## grab the first paramiter passed, we use this as a time for the loop
timetowait = int(sys.argv[1])
cacheoffset = int(sys.argv[2])
notifyonruns = int(sys.argv[3])
123456789
## enter the corresponding information from your Twitter application:
CONSUMER_KEY = '123456789'#keep the quotes, replace this with your consumer key
CONSUMER_SECRET = '123456789'#keep the quotes, replace this with your consumer secret key
ACCESS_KEY = '123456789'#keep the quotes, replace this with your access token
ACCESS_SECRET = '123456789'#keep the quotes, replace this with your access token secret
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

## enter database connection information
dbconfig = {
  'user': 'bot-twitter',
  'password': 'SomeSecurePassword',
  'host': '127.0.0.1',
  'database': 'twitterbot',
  'raise_on_warnings': True,
}

## this is the main function of the program
## accepts a databse configuiration and a time to wait between loops
def mainloop(dbconfig, waitTime):

    ## create counter variables
    i = 0
    j = 0
    k = 0

    ## variable used in db cache cooldown time
    ## we remove 5 seconds to ensure that the next time it's called it's not
    ## the same - we're not working with millisecond accuracy globally
    cachetill = datetime.datetime.now() - datetime.timedelta(seconds=5)

    print('Starting program...')
    print("Paramiters used: loop sleep - %d seconds, connection cache offset - %d seconds , notify every - %d runs" % (waitTime, cacheoffset, notifyonruns))

    ## Infinate loop
    while True:

        ## increment loop counter
        i += 1
        j += 1
        if j / notifyonruns == 1:
            print bcolors.BOLD + "Iteration number: %d" % (i) + bcolors.ENDC
            j = 0

        ## rather than connect to the database each and every time we'll do
        ## some caching to prevent unneccesary connection opening and closing

        ## get time now
        timenow = datetime.datetime.now()

        if cachetill < timenow:

            print( bcolors.OKBLUE + 'making new connection at %s' % (timenow) + bcolors.ENDC)

            ## set next cachetime to time now + the cache offset specified as
            ## arg2 when starting the program
            cachetill = datetime.datetime.now() + datetime.timedelta(seconds=cacheoffset)

            ## connect to the database and set a cursor point
            cnx = dbconnect.dbconnect(dbconfig)
            cursor = dbconnect.dbcursor(cnx)

        ## query for ScheduledTweets that are not sent yet
        selectQuery = ("SELECT id, tweetcontent, timetosend, sent FROM ScheduledTweets WHERE sent = 0")

        ## execute the query and return the result to an array
        cursor.execute(selectQuery)
        selectResult = cursor.fetchall()


        ## loop through the results
        for (id, tweetcontent, timetosend, send) in selectResult:
            ## if not sent yet
            if send == 0:

                #print("Send At: {}, {}".format(timetosend, tweetcontent, send))

                ## get current system time
                timestamp = datetime.datetime.now()
                ## compair current time agains timetosend from the entry
                if timestamp > timetosend :

                    print( bcolors.BOLD + bcolors.HEADER + 'will be sending now' + bcolors.ENDC + bcolors.ENDC)
                    ## set a query to set this entry sent value to 1
                    updateQuery = ("UPDATE ScheduledTweets "
                               "SET sent = '1', "
                               "timesent = NULL "
                               "WHERE id = %d " % (id))

                    ## send the tweet
                    sendtweet(tweetcontent)

                    ## run the update query and commit to the databse
                    cursor.execute(updateQuery)
                    cnx.commit() #commit the changes to the database

                    ## create an INSERT query to copy current tweet to a second
                    ## table for SentTweets
                    insertQuery = ("INSERT INTO SentTweets "
                         "(tweetcontent, timetosend, sent, oldid) "
                         "VALUES "
                         "('%s', '%s', '1', %d)" % (tweetcontent, timetosend, id))

                    ## execute the query and commit to the database
                    cursor.execute(insertQuery)
                    cnx.commit() #commit the changes to the database

            else:
                ## We shouldn't get a result that does == 0. If we do break
                print('There was an error with the queried data.')
                break

        ## print a message between loops
        #print("waiting: %d seconds, already ran: %d times" % (waitTime, i))

        time.sleep(waitTime)

def sendtweet(tweet):
    api.update_status(tweet)

# this is where the program actually starts from
# pass database configuration and a time to wait between loop iterations
mainloop(dbconfig, timetowait)

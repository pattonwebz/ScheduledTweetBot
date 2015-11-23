#!/usr/bin/env python
# bot.py
# description: This is the entry script for a Twitter Bot
# copyrigtht: 2015 William Patton - PattonWebz
# licence: GPLv3
# @package: PWTwitterBot

import tweepy, time, sys, datetime, argparse
# the below imports are imporing other files from this package
import dbconnect
import twitterfunctions
import colors

from configuration import dbconfig

parser = argparse.ArgumentParser()
parser.add_argument("--timetowait", help="time in seconds between how long to wait between loops", default="60", type=int )
parser.add_argument("--cacheoffset", help="time in seconds between mysql connections", default="300", type=int )
parser.add_argument("--notifyonruns", help="issue a message after x runs to show program is still active", default="60", type=int )
parser.add_argument("--user", help="user credentials to use", default="default", type=str )

args = parser.parse_args()

TIMETOWAIT = args.timetowait
CACHEOFFSET = args.cacheoffset
NOTIFYONRNS = args.notifyonruns

authcnx = dbconnect.dbconnect(dbconfig)
authcursor = dbconnect.dbcursor(authcnx)

getKeySecretQuery = ("SELECT CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET FROM Accounts WHERE user = %r" % (args.user))

gotKeySecretResult = authcursor.execute(getKeySecretQuery)

KeySecretResult = authcursor.fetchall()

for (CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET) in KeySecretResult :

    THE_CONSUMER_KEY = CONSUMER_KEY
    THE_CONSUMER_SECRET = CONSUMER_SECRET
    THE_ACCESS_KEY = ACCESS_KEY
    THE_ACCESS_SECRET = ACCESS_SECRET

api = twitterfunctions.authenticatetwitter(THE_CONSUMER_KEY, THE_CONSUMER_SECRET, THE_ACCESS_KEY, THE_ACCESS_SECRET)

# this is the main function of the program
# accepts a databse configuiration and a time to wait between loops
def runner(dbconfig, waitTime):

    ## create counter variables
    i = 0
    j = 0
    k = 0

    ## variable used in db cache cooldown time
    ## we remove 5 seconds to ensure that the next time it's called it's not
    ## the same - we're not working with millisecond accuracy globally
    cachetill = datetime.datetime.now() - datetime.timedelta(seconds=5)

    ## get an api object and asign it to a variable

    authenticated_api = twitterfunctions.authenticatetwitter(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET)

    print colors.tcolors.BOLD + colors.tcolors.HEADER + "Starting program..." + colors.tcolors.ENDC + colors.tcolors.ENDC
    print("Paramiters used: loop sleep - %s seconds, connection cache offset - %s seconds , notify every - %s runs" % (colors.tcolors.GREEN + str(waitTime) + colors.tcolors.ENDC, colors.tcolors.GREEN + str(CACHEOFFSET) + colors.tcolors.ENDC, colors.tcolors.GREEN + str(NOTIFYONRNS) + colors.tcolors.ENDC))

    ## Infinate loop
    while True:

        ## increment loop counter
        i += 1
        j += 1
        if j / NOTIFYONRNS == 1:
            print colors.tcolors.BOLD + "Iteration number: %d" % (i) + colors.tcolors.ENDC
            j = 0

        ## rather than connect to the database each and every time we'll do
        ## some caching to prevent unneccesary connection opening and closing

        ## get time now
        timenow = datetime.datetime.now()

        if cachetill < timenow:

            print( colors.tcolors.BLUE + 'making new connection at %s' % (timenow) + colors.tcolors.ENDC)

            ## set next cachetime to time now + the cache offset specified as
            ## arg2 when starting the program
            cachetill = datetime.datetime.now() + datetime.timedelta(seconds=CACHEOFFSET)

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
                    ## if current time is after scheduled time to send
                    print( colors.tcolors.BOLD + colors.tcolors.HEADER + 'will be sending now' + colors.tcolors.ENDC + colors.tcolors.ENDC)

                    ## set a query to set this entry sent value to 1
                    updateQuery = ("UPDATE ScheduledTweets "
                               "SET sent = '1', "
                               "timesent = NULL "
                               "WHERE id = %d" % (id))

                    ## send the tweet
                    twitterfunctions.sendtweet(authenticated_api, tweetcontent)

                    ## run the update query and commit to the databse
                    cursor.execute(updateQuery)
                    cnx.commit() #commit the changes to the database

                    ## create an INSERT query to copy current tweet to a second
                    ## table for SentTweets
                    insertQuery = ('INSERT INTO SentTweets '
                         '(tweetcontent, timetosend, sent, oldid) '
                         'VALUES '
                         '("%s", "%s", "1", %d)' % (tweetcontent, timetosend, id))

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

def main():
    # this is the main function for the program.

    # pass a dbconfig and a loop time to the main runner
    runner(dbconfig, TIMETOWAIT)

if  __name__ =='__main__':
    main()

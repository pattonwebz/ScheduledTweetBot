#!/usr/bin/env python
# add.py
# description: This is the script for adding scheduled tweets to the database
# copyrigtht: 2015 William Patton - PattonWebz
# licence: GPLv3
# @package: PWTwitterBot

import time, sys, datetime, argparse, re
# the below imports are imporing other files from this package
import dbconnect
from configuration import dbconfig

# start a parser
parser = argparse.ArgumentParser()

# these are the default running arguments
parser.add_argument("--tweetcontent", help="the tweet content", default="")
parser.add_argument("--tweettime", help="time to send the tweet at", default="")
parser.add_argument("--tweettype", help="either a tweet or a retweet", default="tweet")

args = parser.parse_args()

TWEETCONTENT = args.tweetcontent
TWEETTIME = args.tweettime
TWEETTYPE = args.tweettype

def checkInput(tweetContent, tweetTime, tweetType):

    if ( tweetType == "tweet" or tweetType == "retweet" ) :
        # we have the correct tweetType, continue
        if tweetContent == "" :
            print('tweetContent is empty, enter the tweet:')
            tweetContent = raw_input('tweet=')

        if tweetTime == "" :
            print('tweetTime is empty, enter the date and time to send in yyyy-mm-dd hh:mm format')
            tweetTime = raw_input('time=')

        tweetValid = tweetValidate(tweetContent, tweetType)
        timeValid = timeValidate(tweetTime)
        if (tweetValid == False or timeValid == False) :
            return (tweetContent, tweetTime, tweetType)
        else :
            print("something was invalid")

    else :
        # we need to break here - wrong tweetType is a problem we can't
        # automatically overcome or bypass in a sane, user-friendly, way
        print('Error in checkInput')

def tweetValidate(tweet_text, tweet_type):

    # should get the max t.co length from a GET request sent to help/configuration
    # hardcoded at 20 for now.
    # perhaps not a good idea to get the max length here, a seporate function???
    MAXTCOLENGTH = 20
    charCount = len(tweet_text)

    if ( tweet_type == 'retweet' and charCount > 16 ) :
        print ("error with retweet length")

    if charCount > 140 :
        # longer than 140 characters, do some additional checks
        print('over 140 chars')

        ## extract urls from the text using regex
        # bug: this fails to capture the full url when a '#' appears
        # bug: needs the 'http'/'https' - we should check for just 'www.'' too
        urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', tweet_text)

        for (url) in urls:
            urlLength = len(url)
            if urlLength < MAXTCOLENGTH :
                charCount = charCount - urlLength
            else :
                charCount = (charCount - urlLength) + MAXTCOLENGTH

            if charCount < 141 :
                # character count now fits, break.
                print("Tweet length now fits")

            else :
                print( "Tweet too long. Length: %d" % (charCount) )
                return True

        #end for loop

    else :
        # less than 140 characters, should be good to continue
        print('less than 140 chars')

    try:
        charCount < 140;
        return False
    except:
        raise ValueError("Bad Tweet lengh, should be under 140 chars.")

def timeValidate(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d %H:%M')
        return False

    except ValueError:
        raise ValueError("Incorrect date format, should be YYYY-MM-DD HH:MM")

def main():
    # this is the main function for the program.
    global TWEETCONTENT, TWEETTIME, TWEETTYPE
    #print('%s' % (TWEETCONTENT))
    #print('%s' % (TWEETTIME))
    #print('%s' % (TWEETTYPE))
    tweetContent, tweetTime, tweetType = checkInput(TWEETCONTENT, TWEETTIME, TWEETTYPE)

    ## connect to the database and set a cursor point
    cnx = dbconnect.dbconnect(dbconfig)
    cursor = dbconnect.dbcursor(cnx)

    insertQuery = ('INSERT INTO ScheduledTweets '
                 '(tweetcontent, timetosend, sent, done, tweettype) '
                 'VALUES '
                 '("%s", "%s", "0", "0", "%s")' % (tweetContent, tweetTime, tweetType))

    ## run the query and commit to the databse if no error is reported

    cursor.execute(insertQuery)
    cnx.commit() #commit the changes to the database

if  __name__ =='__main__':
    main()

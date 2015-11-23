#!/usr/bin/env python
# setup.py
# description: Very quick and dirty setup script to create tables in DB
# copyrigtht: 2015 William Patton - PattonWebz
# licence: GPLv3
# @package: PWTwitterBot

import dbconnect
from configuration import dbconfig

def dropTableFunction(cursor, query):
    try :
        cursor.execute(query)
    except :
        print("Doesn't exist, will create.")
    else :
        print("Dropped")

def getDefaultKeys(cursor):
    print("Enter the access credentials for the default user account.")
    inConsumerKey = raw_input('Consumer Key = ')
    inConsumerSecret = raw_input('Consumer Secret = ')
    inAccessKey = raw_input('Access Key = ')
    inAccessSecret = raw_input('Access Secret = ')

    insertAccountQuery = ('INSERT INTO Accounts '
                 '(user, CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET) '
                 'VALUES '
                 '("default", "%s", "%s", "%s", "%s")' % (inConsumerKey, inConsumerSecret, inAccessKey, inAccessSecret))
    cursor.execute(insertAccountQuery)
    
def main():

    cnx = dbconnect.dbconnect(dbconfig)
    cursor = dbconnect.dbcursor(cnx)


    dropQuery_Accounts = ('DROP TABLE IF EXISTS Accounts')
    createQuery_Accounts = ('CREATE TABLE Accounts ('
                                'id int(4) unsigned NOT NULL AUTO_INCREMENT, '
                                'user varchar(32) NOT NULL, '
                                'CONSUMER_KEY varchar(140) NOT NULL, '
                                'CONSUMER_SECRET varchar(140) NOT NULL, '
                                'ACCESS_KEY varchar(140) NOT NULL, '
                                'ACCESS_SECRET varchar(140) NOT NULL, '
                                'PRIMARY KEY (id))'
                            )
    dropTableFunction(cursor, dropQuery_Accounts)
    cursor.execute(createQuery_Accounts)

    dropQuery_ScheduledTweets = ('DROP TABLE IF EXISTS ScheduledTweets')
    createQuery_ScheduledTweets = ('CREATE TABLE ScheduledTweets ('
                                    'id int(6) unsigned NOT NULL AUTO_INCREMENT, '
                                    'tweetcontent blob NOT NULL, '
                                    'timetosend datetime NOT NULL, '
                                    'sent tinyint(1) NOT NULL, '
                                    'timesent timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, '
                                    'done tinyint(1) NOT NULL, '
                                    'tweettype varchar(16) NOT NULL DEFAULT "tweet", '
                                    'PRIMARY KEY (id))'
                                )
    dropTableFunction(cursor, dropQuery_ScheduledTweets)
    cursor.execute(createQuery_ScheduledTweets)

    dropQuery_SearchedForTweets = ('DROP TABLE IF EXISTS SearchedForTweets')
    createQuery_SearchedForTweets = ('CREATE TABLE SearchedForTweets ('
                                        'id int(6) unsigned NOT NULL AUTO_INCREMENT, '
                                        'tweetid varchar(20) NOT NULL, '
                                        'username varchar(20) NOT NULL, '
                                        'tweetcontent varchar(1024) NOT NULL, '
                                        'timesent datetime NOT NULL, '
                                        'searchterm varchar(128) DEFAULT NULL, '
                                        'PRIMARY KEY (id), '
                                        'UNIQUE KEY id (id), '
                                        'UNIQUE KEY tweetid (tweetid))'
                                    )
    dropTableFunction(cursor, dropQuery_SearchedForTweets)
    cursor.execute(createQuery_SearchedForTweets)


    dropQuery_SentTweets = ('DROP TABLE IF EXISTS SentTweets')
    createQuery_SentTweets = ('CREATE TABLE SentTweets ('
                                        'id int(6) unsigned NOT NULL AUTO_INCREMENT, '
                                        'tweetcontent varchar(140) NOT NULL, '
                                        'timetosend datetime NOT NULL, '
                                        'oldid int(6) NOT NULL DEFAULT 202, '
                                        'sent tinyint(1) NOT NULL, '
                                        'timesent timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, '
                                        'PRIMARY KEY (id))'
                                    )

    dropTableFunction(cursor, dropQuery_SentTweets)
    cursor.execute(createQuery_SentTweets)

    getDefaultKeys()

    cnx.commit()

if  __name__ =='__main__':
    main()

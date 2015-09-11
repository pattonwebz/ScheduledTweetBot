# ScheduledTweetBot
A Scheduled Tweet bot written in Python to run on a Raspberry Pi (runs anywhere Python and the dependencies are installed).

## Usage
Running is simple: run the script passing 3 arguments

=======
1. Time between send loops - this will dictate responsiveness of the bot.
2. A time between new connections to the database - this will reduce reads to the FS with a higher value but may not discover new tweets that are added between (connection cache offset + time between loops).
3. An amount of times to run before outputing a notice it's still running - Once I was sure it was working I wanted to see less notifications on screen.

```
python bot.py 60 300 15
```

The above command runs the bot, loops it every 60 seconds, makes fresh database connections every 300 seconds and only says it's stil running after 15 loops

##Setup
Edit the `bot.py` file and enter your database and Twitter credentials. It uses a database structure like with 2 tables - ScheduledTweets and SentTweets

```
CREATE TABLE SentTweets (
    id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    tweetcontent VARCHAR(140) NOT NULL,
    timetosend DATETIME NOT NULL,
    oldid INT(6) NOT NULL DEFAULT='0',
    sent TINYINT(1) NOT NULL DEFAULT='0'
    timesent TIMESTAMP
);
```

```
CREATE TABLE ScheduledTweets (
    id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    tweetcontent VARCHAR(140) NOT NULL,
    timetosend DATETIME NOT NULL,
    sent TINYINT(1) NOT NULL,
    timesent TIMESTAMP
);
```
### Credits
Uses the 'Tweepy' library for all Twitter API actions. http://github.com/tweepy/tweepy

Tweepy is released under the MIT licence (GPL compatable)

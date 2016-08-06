# ScheduledTweetBot
A Scheduled Tweet bot written in Python to run on a Raspberry Pi (runs anywhere Python and the dependencies are installed).

## Usage
Run the bot with the command `python bot.py`.

The above command runs the bot, loops it every 60 seconds, makes fresh database connections every 300 seconds and only says it's stil running after 15 loops. You can edit the default values, just use `python bot.py --help` to see all options.

## Requirements

Requires you install mysql-connector and Tweepy.

Download mysql-connecter from here: https://dev.mysql.com/downloads/connector/python/

If you're using this on a RPi then you'll likely want the architecture independant .deb file.

You can install Tweepy using pip, easy_install or any other method that gets it's pacages from PyPy:

`pip install tweepy`

##Setup

Edit the "configuration.py" file and enter your database credentials then run the setup script with `python setup.py`.

It will promt you to enter your Twitter credentials - Consumer Key & Secret, Access Token & Secret

##Scheduling Tweets
Add some scheduled tweets by calling the "add.py" script.

"""
python add.py
"""
You can pass some args like so:

"""
python add.py --tweetcontent="this is the tweet" --tweettime="2015-12-25 00:00"
"""

### Credits
Uses the 'Tweepy' library for all Twitter API actions. http://github.com/tweepy/tweepy

Tweepy is released under the MIT licence (GPL compatable)

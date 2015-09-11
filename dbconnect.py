#!/usr/bin/env python
# dbconnect.py
# description: A simple MySQL database connection module
# copyrigtht: 2015 William Patton - PattonWebz
# licence: GPLv3
# @package: PWTwitterBot
# @subpackage: DBConnect

import mysql.connector
from mysql.connector import errorcode

def dbconnect(config):
  # note: returning cnx effectively closes the connection
  try:
    cnx = mysql.connector.connect(**config)

  except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
      print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
      print("Database does not exist")
    else:
      print(err)

  else:
    return cnx

def dbcursor(cnx):

  cursor = cnx.cursor()
  return cursor


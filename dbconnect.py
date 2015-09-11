import mysql.connector
from mysql.connector import errorcode

config = {
  'user': 'bot-twitter',
  'password': 'SomeSecurePassword',
  'host': '127.0.0.1',
  'database': 'twitterbot',
  'raise_on_warnings': True,
  'pool_size' : 2
}

def dbconnect(config):


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

def dbclose(cnx):
  cnx.close()

def dbcursor(cnx):
  cursor = cnx.cursor()
  return cursor

def dbcursorclose(cursor):
  cursor.close()

import sqlite3
from os.path import expanduser


def db_cursor():
    conn = sqlite3.connect(expanduser("~") +
                           "/PycharmProjects/banking/data/forecast.sqlite")
    return conn.cursor()

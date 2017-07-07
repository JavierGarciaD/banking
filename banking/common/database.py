import sqlite3
from os.path import expanduser


def conection():

    conn = sqlite3.connect(expanduser("~") +
                           "/git/banking/data/forecast.sqlite")

    cur = conn.cursor()
    cur.execute("select * from scores")
    results = cur.fetchall()

    for each_item in results:
        print(each_item[0])


if __name__ == '__main__':
    conection()

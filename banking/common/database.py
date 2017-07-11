import os
import sqlite3

import definitions


def conection():
    root = definitions.root_dir()
    db_root = os.path.join(root, "data", "forecast.sqlite")

    conn = sqlite3.connect(db_root)
    cur = conn.cursor()
    cur.execute("select * from credit")
    results = cur.fetchall()

    for each_item in results:
        print(each_item)


if __name__ == '__main__':
    conection()

import sqlite3
with sqlite3.connect("clubs.db") as conn:
    cur = conn.cursor()
    print(cur.execute('SELECT * FROM user;').fetchall())


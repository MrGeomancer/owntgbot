import mainparsing
import sqlite3

with sqlite3.connect('database.db') as db:
    cursor= db.cursor()

    cursor.execute("""CREATE TABLE articles(
    id INTEGER,
    url TEXT,
    name TEXT,
    price TEXT
    )""")

    cursor.execute("INSERT INTO")


# mainparsing.parsing()
import sqlite3
import traceback
import re

with sqlite3.connect('database.db') as db:
    cursor = db.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS cases(
    caseid INTEGER PRIMARY KEY,
    userid TEXT,
    url TEXT,
    token TEXT,
    name TEXT,
    price REAL DEFAULT (0) 
    )""")
    # cursor.execute('SELECT price FROM cases WHERE url = ?', ['qq'])
    # caseid = cursor.fetchone()[0]
    # cursor.execute('ALTER TABLE cases ADD COLUMN userid "TEXT"')

def profileprint(tgid):
    d = {}
    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()
        cursor.execute('SELECT caseid, name, price FROM cases WHERE userid = ?', [tgid])
        a = cursor.fetchall()
        # print(a[0][0])
        for i in range(len(a)):
            d[a[i][0]] = []
            d[a[i][0]].append(a[i][1])
            d[a[i][0]].append(a[i][2])
            # print(d[i + 1])
    return d

def deletecase1(tgid):
    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()
        cursor.execute('SELECT caseid, name FROM cases WHERE userid = ?', [tgid])
        a = cursor.fetchall()
        return a

def deletecase2(msg):
    message = re.findall(r"\d+", msg.text)[0]
    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()
        try:
            cursor.execute("DELETE FROM cases WHERE caseid = ? AND userid = ?", [message, msg.from_user.id])
            db.commit()
            res = 'Готово 🥰'
        except:
            res = 'Не правильно был указан ID кейса'
        return res

if __name__ == "__main__":
    d = []
    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()
        cursor.execute('SELECT caseid, name FROM cases WHERE userid = ?', [353170432])
        a = cursor.fetchall()
        print(a)
        # for i in range(len(a)):
        #     d[a[i][0]] = []
        #     d[a[i][0]].append(a[i][1])
        #     d[a[i][0]].append(a[i][2])
        print(a[0][1])
    pass
import sqlite3
import traceback

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


if __name__ == "__main__":
    d = {}
    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()
        cursor.execute('SELECT caseid, name, price FROM cases WHERE userid = ?', [353170432])
        a = cursor.fetchall()
        # print(a[0][0])
    for i in range(len(a)):
        d[a[i][0]] = []
        d[a[i][0]].append(a[i][1])
        d[a[i][0]].append(a[i][2])
        # print(d[i + 1])
    b = (len(d))
    #print(str(d[2 + 1][1]))
    #sst = str(d[0 + 1][0]) + ' купленный за ' + str(d[0 + 1][0 + 1]) + ' рублей.'
    sst = '\n'
    for ind in range(len(d)):
        sst = sst+str(d[ind+1][0])+' купленный за '+str(d[ind+1][1])+' рублей\n'

    print(sst)
    pass
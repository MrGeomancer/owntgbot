import sqlite3
import traceback

with sqlite3.connect('database.db') as db:
    cursor = db.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS cases(
    id INTEGER PRIMARY KEY,
    url TEXT,
    token TEXT,
    name TEXT,
    price REAL
    )""")
    # cursor.execute('ALTER TABLE cases ADD COLUMN token "TEXT"')
    # url = input('Дай ссылку на кейс: ')
    # cursor.execute('SELECT id FROM cases WHERE url = ?', [url])
    # print(cursor.fetchone()[0])
    # cursor.execute ("INSERT INTO")


def caseadd():
    url = input('Дай ссылку на кейс: ')
    try:
        price = float(str(input('За сколько ты его покупал?: ')).replace(",", '.'))
    except:
        print('дурачок? только числа вводи')
        try:
            price = float(str(input('За сколько ты его покупал?: ')).replace(",", '.'))
        except ValueError:
            print('Пошел нахуй')
            return
    try:
        db = sqlite3.connect('database.db')
        cursor = db.cursor()
        cursor.execute("SELECT url FROM cases WHERE url = ?", [url])
        if cursor.fetchone() is None:
            cursor.execute('INSERT INTO cases(url, price) VALUES(?, ?)', [url, price])
            db.commit()
        else:
            cursor.execute('SELECT id FROM cases WHERE url = ?', [url])
            caseid = cursor.fetchone()[0]
            print('Этот кейс уже записан и имеет находится под id', caseid, 'в датабазе')
            if input('Хотите изменить цену его закупки? Да/Нет: ') == 'Да':
                cursor.execute('UPDATE cases SET price = ? WHERE url = ?', [price, url])
                db.commit()
                print('**Выполнено**')
            else:
                print('Ты сука?')
                caseadd()
    except sqlite3.Error as e:
        print('иди нахуй')
        print('Ошибка:\n', traceback.format_exc())
    finally:
        cursor.close()
        db.close()

if __name__ == "__main__":
    caseadd()
    # mainparsing.parsing()

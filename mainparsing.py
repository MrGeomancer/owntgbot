import requests
import re
from bs4 import BeautifulSoup
import json
import sqlite3
import traceback

headers = {

    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'ru-UA,ru;q=0.9,en-US;q=0.8,en;q=0.7,ru-RU;q=0.6'}

# url = [
#     'https://steamcommunity.com/market/listings/730/Spectrum%20Case',
#     'https://steamcommunity.com/market/listings/730/Snakebite%20Case',
#     'https://steamcommunity.com/market/listings/730/Autograph%20Capsule%20%7C%20Legends%20%28Foil%29%20%7C%20MLG%20Columbus%202016'
#
# ]


def parsing(url):
    try:
        r = requests.get(url, headers=headers)
    except:
        print('Сервер не подключен к интернету')
        return
    try:
        soup = BeautifulSoup(r.text, "html.parser")
        return soup
    except requests.exceptions.ConnectionError:
        print('Неизвестная шибка')


def takenames(tgid):
    url=[]
    caseid=[]
    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()
        cursor.execute('SELECT url FROM cases WHERE userid = ?', [tgid])
        a = cursor.fetchall()
        try:
            for i in range(len(a)):
                url.append(a[i][0])
            cursor.execute('SELECT caseid FROM cases WHERE userid = ?', [tgid])
            a = cursor.fetchall()
            for i in range(len(a)):
                caseid.append(a[i][0])
            for i in range(len(url)):
                soup = parsing(url[i])
                qquotes = soup.find('span', class_='market_listing_item_name').text
                cursor.execute("UPDATE cases SET name = ? WHERE userid = ? AND caseid = ?", [qquotes, tgid, caseid[i]])
                res = 'Ок'
        except:
            print(traceback.format_exc())
            res = 'Не ок'
        return res

def taketokens(tgid):
    url = []
    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()
        cursor.execute('SELECT url FROM cases WHERE userid = ?', [tgid])
        a = cursor.fetchall()
        try:
            for i in range(len(a)):
                url.append(a[i][0])
            for i in url:
                r = requests.get(i, headers=headers)
                soup = BeautifulSoup(r.text, "html.parser")
                quotes = soup.findAll('script')
                itemActivityTickerStart = re.findall(r"(?<=\( )\d+", str(quotes), flags=re.IGNORECASE)[2]
                cursor.execute("UPDATE cases SET token = ? WHERE url = ?", [itemActivityTickerStart, i])
                db.commit()
                res = 'Ок'
        except:
            print(traceback.format_exc())
            res = 'Не ок'
    return res

def takeprice(tgid):
    token = []
    price = []
    floatprice = []
    oldprice = []
    ttext = '\n'
    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()
        cursor.execute('SELECT token, name FROM cases WHERE userid = ?', [tgid])
        a = cursor.fetchall()
    try:
        for i in range(len(a)):
            token.append(a[i][0])
        for i in range(len(token)):
            price_update2 = 'https://steamcommunity.com/market/itemordershistogram?country=RU&language=russian&currency=5&item_nameid=%s&two_factor=0' \
                            % token[i]
            r2 = requests.get(price_update2, 'html.parser')
            str_json = str(r2.text)
            data = json.loads(str_json)
            sosoup = BeautifulSoup(data['buy_order_summary'], "html.parser")
            ququotes = sosoup.find_all('span', class_="market_commodity_orders_header_promote")[1].text
            price.append(ququotes)
            floatprice.append(re.findall(r"\d+,\d+", ququotes)[0])
            floatprice[i] = floatprice[i].replace(',', '.')
        with sqlite3.connect('database.db') as db:
            cursor = db.cursor()
            cursor.execute('SELECT price FROM cases WHERE userid = ?', [tgid])
            b = cursor.fetchall()
            for i in range(len(b)):
                oldprice.append(b[i][0])
        for i in range(len(price)):
            if float(floatprice[i]) > float(oldprice[i]):
                x = round(((float(floatprice[i]))/float(oldprice[i])), 1)
                s = '🟢 Выгода: <b>x' + str(x) + '!</b>'
            else:
                x = round(((float(oldprice[i]/float(floatprice[i])))), 1)
                s = '🟥 Потери в <b>' + str(x) + '</b> раз...'
            ttext = ttext + str(i + 1) + '.' + str(a[i][1]) + ' сейчас можно купить за <b>' + price[
                i] + '</b>' + s + '\n'
        return ttext
    except:
        print(traceback.format_exc())
        return 'Не ок'

def takeprice2(itemActivityTickerStart):
    price_update2 = 'https://steamcommunity.com/market/itemordershistogram?country=RU&language=russian&currency=5&item_nameid=%s&two_factor=0' \
                   % itemActivityTickerStart
    r2 = requests.get(price_update2, 'html.parser')

    str_json = str(r2.text)
    data = json.loads(str_json)
    sosoup = BeautifulSoup(data['buy_order_summary'], "html.parser")
    ququotes = sosoup.find_all('span', class_="market_commodity_orders_header_promote")[1].text
    print(ququotes)
    return r2.text

if __name__ == "__main__":

    # headers_mobile = {
    #     'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B137 Safari/601.1'}
    #
    # url = 'https://www.sberbank.ru/proxy/services/rates/public/actual?rateType=ERNP-2&isoCodes[]=USD&isoCodes[]=EUR'
    # r = requests.get(url,headers=headers_mobile)
    # soup = BeautifulSoup(r.text, "lxml")
    # quotes = soup.find_all('div', class_="bp-container bp-ui-dragRoot bp-manageableArea --area bp-area")
    # rson = str(r.text)
    # #data = json.loads(rson)
    # print(r.text)
    pass



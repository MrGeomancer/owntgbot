import requests
import re
from bs4 import BeautifulSoup
import json

headers = {

    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'ru-UA,ru;q=0.9,en-US;q=0.8,en;q=0.7,ru-RU;q=0.6'}

url = [
    'https://steamcommunity.com/market/listings/730/Spectrum%20Case',
    'https://steamcommunity.com/market/listings/730/Snakebite%20Case',
    'https://steamcommunity.com/market/listings/730/Autograph%20Capsule%20%7C%20Legends%20%28Foil%29%20%7C%20MLG%20Columbus%202016'

]


def parsing():
    for i in url:
        try:
            r = requests.get(i, headers=headers)
        except:
            print('Сервер не подключен к интернету')
            break
        try:
            soup = BeautifulSoup(r.text, "html.parser")
            takeprice(soup)
        except requests.exceptions.ConnectionError:
            print('Неизвестная шибка')


def takeprice(soup):
    quotes = soup.findAll('script')
    itemActivityTickerStart = re.findall(r"(?<=\( )\d+", str(quotes), flags=re.IGNORECASE)
    takeprice2(itemActivityTickerStart[2])


def takeprice2(itemActivityTickerStart):
    price_update2 = 'https://steamcommunity.com/market/itemordershistogram?country=RU&language=russian&currency=5&item_nameid=%s&two_factor=0' \
                   % itemActivityTickerStart
    r2 = requests.get(price_update2, 'html.parser')

    str_json = str(r2.text)
    data = json.loads(str_json)
    sosoup = BeautifulSoup(data['buy_order_summary'], "html.parser")
    ququotes = sosoup.find_all('span', class_="market_commodity_orders_header_promote")[1].text
    print(ququotes)






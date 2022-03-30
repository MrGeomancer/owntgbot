import requests
import re
import time


def takeprice(r):
    for i in r.text.split(';'):
        if "ItemActivityTicker.Start" in i:
            ItemActivityTickerStart = (re.search(r"\d+", i).group(0))
            takeprice2(ItemActivityTickerStart)
            break


def takeprice2(ItemActivityTickerStart):
    PriceUpdate = 'https://steamcommunity.com/market/itemordershistogram?country=RU&language=russian&currency=5&item_nameid=%s&two_factor=0'\
                  % (ItemActivityTickerStart)
    r = requests.get(PriceUpdate, headers=headers)
    for i in r.text.split('","'):
        if "market_commodity_orders_header_promote" and 'buy_order_summary' in i:
            cen = re.search(r"\d+[,|.]\d{2}", i).group(0)
            break
    val = eval(str(r.text.split(',')[-2:])
               .replace("'", '').replace(" ", '').replace('}', '').replace('[', "{").replace(']', "}"))
    print(val['price_prefix']+cen+' '+val['price_suffix'])

start_time = time.time()
headers = {

    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'ru-UA,ru;q=0.9,en-US;q=0.8,en;q=0.7,ru-RU;q=0.6'}

url = [
    'https://steamcommunity.com/market/listings/730/Spectrum%20Case',
    'https://steamcommunity.com/market/listings/730/Snakebite%20Case',
    'https://steamcommunity.com/market/listings/730/Autograph%20Capsule%20%7C%20Legends%20%28Foil%29%20%7C%20MLG%20Columbus%202016'

        ]
# print (dict.fromkeys(url))



for i in url:
    r = requests.get(i, headers=headers)
    takeprice(r)

print(f"{(time.time() - start_time)*1} секунд")

import requests
import re
from bs4 import BeautifulSoup
import json





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

headers = {

    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'ru-UA,ru;q=0.9,en-US;q=0.8,en;q=0.7,ru-RU;q=0.6'}

# USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
# MOBILE_USER_AGENT = "Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36"
# headers = {"user-agent" : MOBILE_USER_AGENT}
url = [
    'https://steamcommunity.com/market/listings/730/Spectrum%20Case',
    'https://steamcommunity.com/market/listings/730/Snakebite%20Case',
    'https://steamcommunity.com/market/listings/730/Autograph%20Capsule%20%7C%20Legends%20%28Foil%29%20%7C%20MLG%20Columbus%202016'

]
# print (dict.fromkeys(url))
# for i in url:
#     r = requests.get(i, headers=headers)
#     takeprice(r)


# uu = 'https://steamcommunity.com/market/listings/730/Spectrum%20Case'
# p = requests.get(uu, headers=headers)
# print (p.text)
# for i in p.text.split(';'):
#     if "ItemActivityTicker.Start" in i:
#         ItemActivityTickerStart = (re.search(r"\d+", i).group(0))
#         takeprice2(ItemActivityTickerStart)
#         break


# это длинный вариант того, как работает принт ниже
# z = str(soup).split('Начальная цена:')
# print (z)
# x = z[2]
# print (x)
# c = (x.split('.&lt;')[0])
# print(c.split('>')[1])
#
# это укороченный вариант строк выше
# print(str(soup).split('Начальная цена:')[2].split('.&lt;')[0].split('>')[1])
# самый короткий вариант, который возможно перестанет работать раньше, чем верхний
# print(str(soup).split('&lt;')[-2].split('>')[-1])
# print(r.text.split('<\/span>'))
#   человек парсер, работающий только с модулем request и re
# for i in r.text.split('","'):
#     if "market_commodity_orders_header_promote" and 'buy_order_summary' in i:
#         cen = re.search(r"\d+[,|.]\d{2}",i).group(0)
#         break
# val = eval(str(r.text.split(',')[-2:])
#            .replace("'", '').replace(" ", '').replace('}', '').replace('[', "{").replace(']', "}"))
# print(val['price_prefix']+cen+' '+val['price_suffix'])

url2 = 'https://steamcommunity.com/market/listings/730/Snakebite%20Case'
r = requests.get(url2, headers=headers)
soup = BeautifulSoup(r.text, "html.parser")
quotes = soup.findAll('script')
Market_LoadOrderSpread = re.search(r"(?<=\( )\d+", str(quotes)).group(0)
PriceUpdate2 = 'https://steamcommunity.com/market/itemordershistogram?country=RU&language=russian&currency=5&item_nameid=%s&two_factor=0'\
                  % (Market_LoadOrderSpread)
r2 = requests.get(PriceUpdate2, 'html.parser')

str_json = str(r2.text)
data = json.loads(str_json)
sosoup = BeautifulSoup(data['buy_order_summary'], "html.parser")
ququotes = sosoup.findAll('span', class_="market_commodity_orders_header_promote")
print(ququotes[1])
#print(data['buy_order_summary'])
#print(type(sosoup))
q = ququotes[1].text
print(q)





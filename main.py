import mainparsing
import maindatabasecode
import telegramkey
import telebot
import sqlite3
import traceback
import time
from telebot import types

bot = telebot.TeleBot(telegramkey.bot)
messageid = None
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton("👨‍🏫 Мой профиль")
    btn2 = types.KeyboardButton("💼 Добавить кейс")
    btn3 = types.KeyboardButton("📈 Посмтреть на кейсы")
    btn4 = types.KeyboardButton("📈 Посмотреть на валюты")
    btn5 = types.KeyboardButton("🛒 Сравнить цены")
    markup.add(btn1, btn2, btn3, btn4, btn5)
    if message.text == '/start':
        bot.send_message(message.chat.id,
                         text="Дарова кликай на кнопки и все будет круто💪👀👍".format(message.from_user),
                         reply_markup=markup)
    else:
        bot.send_message(message.chat.id,
                         text="Добро пожаловать домой💪👀👍".format(message.from_user),
                         reply_markup=markup)

@bot.message_handler(content_types=['text'])
def buttons(message):
    if (message.text == "👨‍🏫 Мой профиль"):
        myprofile(message)
    elif (message.text == "💼 Добавить кейс"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("⭕️Вернуться в главное меню"))
        msg = bot.send_message(message.chat.id, text="Давай ссылку на кейс", reply_markup=markup)
        bot.register_next_step_handler(msg, handler_url)
    elif (message.text == "📈 Посмтреть на кейсы"):
        bot.send_message(message.chat.id, text="Пока пусто")

    elif message.text == "📈 Посмотреть на валюты":
        bot.send_message(message.chat.id, text="Пока пусто")

    elif (message.text == "⭕️Вернуться в главное меню" or '⚪️Вернуться в главное меню'):
        start(message)
    elif (message.text == '🛒 Сравнить цены'):
        bot.send_message(message.chat.id, text="Пока пусто")
    else:
        bot.send_message(message.chat.id, text="На такую комманду я не запрограммировал..")
        pass
    print ('%s | @%s | %s'% (time.strftime('%H:%M:%S %d.%m'), message.from_user.username, message.text))

def myprofile(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton("❕️Обновить названия")
    btn2 = types.KeyboardButton("❔️Настроить токены")
    btn3 = types.KeyboardButton("⭕️Вернуться в главное меню")
    btn4 = types.KeyboardButton('❌ Удалить кейсы')
    markup.add(btn1, btn2, btn3, btn4)
    d = maindatabasecode.profileprint(message.from_user.id)
    v = list(d.keys())
    sst = '\n'
    for ind in range(len(d)):
        sst = sst + '<b>' + str(d[v[ind]][0]) + '</b>' + ' купленный за ' + '<b>' + str(
            d[v[ind]][1]) + '</b>' + ' рублей.\n'
    if message.text == '👨‍🏫 Мой профиль':
        msg = bot.send_message(message.chat.id, text=f"""
                Привет {message.from_user.first_name}, твои кейсы:{sst}
                """, reply_markup=markup, parse_mode='html')
    else:
        msg = bot.send_message(message.chat.id, text=f"""Теперь твои кейсы:{sst}
                """,  parse_mode='html', reply_markup=markup)
    bot.register_next_step_handler(msg, handler_profileprint)

def handler_url(message):
    global url
    if message.text == "⭕️Вернуться в главное меню":
        start(message)
        return
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("⭕️Вернуться в главное меню"))
    markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton("✔️Да")
    btn2 = types.KeyboardButton("✖️Нет")
    btn3 = types.KeyboardButton("⭕️Вернуться в главное меню")
    markup2.add(btn1, btn2, btn3)
    url = message.text
    try:
        with sqlite3.connect('database.db') as db:
            cursor = db.cursor()
            cursor.execute("SELECT url FROM cases WHERE url = ? AND userid = ?", [url, message.from_user.id])
            if cursor.fetchone() is None:
                cursor.execute('INSERT INTO cases(url,userid) VALUES(?,?)', [url, message.from_user.id])
                db.commit()
                msg = bot.reply_to(message, 'За сколько ты его покупал?', reply_markup=markup)
                bot.register_next_step_handler(msg, handler_price)
            else:
                cursor.execute('SELECT caseid FROM cases WHERE url = ? AND userid = ?', [url, message.from_user.id])
                caseid = cursor.fetchone()[0]
                cursor.execute('SELECT price FROM cases WHERE url = ? AND userid = ?', [url, message.from_user.id])
                caseprice = str(cursor.fetchone()[0])+' руб.'
                # print(str(cursor.fetchone()[0])+' руб.')
                urltaken = 'Этот кейс уже записан и имеет находится под <b>ID: %s</b> в датабазе\nУстановленная цена:<b>%s</b> Хочешь перезаписать его цену?' % (caseid, caseprice)
                msg = bot.reply_to(message, text=urltaken, reply_markup=markup2, parse_mode='html')
                bot.register_next_step_handler(msg, handler_url_taken)
    except sqlite3.Error as e:
        print('чета ебнуло')
        print('Ошибка:\n', traceback.format_exc())
    finally:
        cursor.close()
        db.close()
        return url

def handler_url_taken(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("⭕️Вернуться в главное меню"))
    if (message.text == "⭕️Вернуться в главное меню"):
        start(message)
        return
    elif message.text == '✔️Да':
        msg = bot.reply_to(message, 'За сколько ты его покупал?', reply_markup=markup)
        bot.register_next_step_handler(msg, handler_price)
    elif message.text == '✖️Нет':
        start(message)
        return

def handler_price(message):
    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()
        if message.text == "⭕️Вернуться в главное меню":
            try:
                cursor.execute("DELETE FROM cases WHERE price = 0 and url = ? and userid = ?",
                               [url, message.from_user.id])
                db.commit()
            except TypeError:
                start(message)
            start(message)
            return
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("⚪️Вернуться в главное меню"))
        try:
            price = message.text
            price = float(price.replace(",", '.'))
            cursor.execute("UPDATE cases SET price = ? WHERE url = ? AND userid = ?", [price, url, message.from_user.id])
            db.commit()
            bot.reply_to(message, 'Готово 🥰', reply_markup=markup)
            start(message)
        except:
            print('чета ебнуло')
            print('Ошибка:\n', traceback.format_exc())
            bot.reply_to(message, 'дурачок? только числа вводи. Теперь начинай все сначала')
            cursor.execute("DELETE FROM cases WHERE url = ? AND userid = ?", [url, message.from_user.id])
            db.commit()
            start(message)

def handler_profileprint(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("❕️Обновить названия")
    btn2 = types.KeyboardButton("❔️Настроить токены")
    btn3 = types.KeyboardButton("⭕️Вернуться в главное меню")
    btn4 = types.KeyboardButton('❌ Удалить кейсы')
    markup.add(btn1, btn2, btn3, btn4)
    markup2.add(btn3)
    if (message.text == "⭕️Вернуться в главное меню"):
        start(message)
        return
    elif message.text == '❕️Обновить названия':
        if mainparsing.takenames(message.from_user.id) == 'Ок':
            bot.reply_to(message, 'Названия добавлены в базу!', reply_markup=markup)
            myprofile(message)
        else:
            bot.reply_to(message, 'Гдето ты напортачил...', reply_markup=markup)
            myprofile(message)
    elif message.text == '❔️Настроить токены':
        start(message)
        return
    elif message.text == '❌ Удалить кейсы':
        caselist = maindatabasecode.deletecase1(message.from_user.id)
        deletecasetext = ''
        for i in range(len(caselist)):
            deletecasetext = deletecasetext + 'ID ' + str(caselist[i][0]) + ': ' + str(caselist[i][1])+'\n'
        msg = bot.reply_to(message, f'Введите числовой ID кейса, который хотите удалить.\n{deletecasetext}', reply_markup=markup2)
        bot.register_next_step_handler(msg, handler_deletecase)

def handler_deletecase(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("⚪️Вернуться в главное меню"))
    if (message.text == "⭕️Вернуться в главное меню"):
        start(message)
        return
    try:
        bot.send_message(message.chat.id, text=maindatabasecode.deletecase2(message))
        time.sleep(0.5)
        myprofile(message)
    except:
        bot.send_message(message.chat.id, text="Ты чото делаешь не так, давай сначала", reply_markup=markup)
        start(message)
        print(traceback.format_exc())
if __name__ == '__main__':
    print('Date | @username | Message text')
    bot.infinity_polling()


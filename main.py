import mainparsing
import maindatabasecode
import telegramkey
import telebot
import sqlite3
import traceback
from time import sleep, strftime
from telebot import types
first_gramm = None
first_price = None
second_gramm = None
second_price = None
bot = telebot.TeleBot(telegramkey.bot)


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton("👨‍🏫 Мой профиль")
    btn3 = types.KeyboardButton("📈 Посмтреть на кейсы")
    btn4 = types.KeyboardButton("📈 Посмотреть на валюты")
    btn5 = types.KeyboardButton("🛒 Сравнить цены")
    markup.add(btn1, btn3, btn4, btn5)
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
    if message.text == "👨‍🏫 Мой профиль":
        myprofile(message)
    elif message.text == "💼 Добавить кейс":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("⭕️Вернуться в главное меню"))
        msg = bot.send_message(message.chat.id, text="Давай ссылку на кейс", reply_markup=markup)
        bot.register_next_step_handler(msg, handler_url)

    elif message.text == "📈 Посмтреть на кейсы" or message.text == '♾ Обновить цены':
        markup3 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        btn1 = types.KeyboardButton("💼 Добавить кейс")
        btn2 = types.KeyboardButton("♾ Обновить цены")
        btn3 = types.KeyboardButton("⭕️Вернуться в главное меню")
        markup3.add(btn1, btn2, btn3)
        takepricemsg = mainparsing.takeprice(message.from_user.id)
        if takepricemsg == 'Не ок':
            sleep(3)
            takepricemsg = mainparsing.takeprice(message.from_user.id)
            if takepricemsg == 'Не ок':
                msg = bot.send_message(message.chat.id, text="Где-то произошла ошибка.", reply_markup=markup3)
        else:
            msg = bot.send_message(message.chat.id, text=takepricemsg, reply_markup=markup3,
                                   parse_mode='html')
        bot.register_next_step_handler(msg, handler_caselookup)

    elif message.text == "📈 Посмотреть на валюты":
        bot.send_message(message.chat.id, text="Пока пусто")

    elif message.text == '🛒 Сравнить цены' or message.text == '↩️Посчитать еще раз':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("⭕️Вернуться в главное меню"))
        msg = bot.send_message(message.chat.id, text="Сколько грамм у первого продукта?.", reply_markup=markup)
        bot.register_next_step_handler(msg, handler_priceculc0)

    elif message.text == "⭕️Вернуться в главное меню" or message.text == '⚪️Вернуться в главное меню':
        start(message)

    else:
        bot.send_message(message.chat.id, text="На такую комманду я не запрограммировал..")
        start(message)
        pass
    print('%s | @%s | %s' % (strftime('%H:%M:%S %d.%m'), message.from_user.username, message.text))


def handler_priceculc0(message):
    global first_gramm
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("⭕️Вернуться в главное меню"))
    if message.text == "⭕️Вернуться в главное меню":
        start(message)
        return
    try:
        first_gramm = float(message.text)
    except:
        bot.send_message(message.chat.id, text='Только цирфы, долбоеб')
        start(message)
    msg = bot.reply_to(message, 'А сколько рублей он стоит?',
                       reply_markup=markup)
    bot.register_next_step_handler(msg, handler_priceculc1)


def handler_priceculc1(message):
    global first_price
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("⭕️Вернуться в главное меню"))
    if message.text == "⭕️Вернуться в главное меню":
        start(message)
        return
    try:
        first_price = float(message.text)
    except:
        bot.send_message(message.chat.id, text='Только цирфы, долбоеб')
        start(message)
    msg = bot.send_message(message.chat.id, 'Сколько грамм у второго продукта?',
                           reply_markup=markup)
    bot.register_next_step_handler(msg, handler_priceculc2)


def handler_priceculc2(message):
    global second_gramm
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("⭕️Вернуться в главное меню"))
    if message.text == "⭕️Вернуться в главное меню":
        start(message)
        return
    try:
        second_gramm = float(message.text)
    except:
        bot.send_message(message.chat.id, text='Только цирфы, долбоеб')
        start(message)
    msg = bot.reply_to(message, 'А сколько рублей он стоит?',
                       reply_markup=markup)
    bot.register_next_step_handler(msg, handler_priceculc3)


def handler_priceculc3(message):
    global first_gramm
    global first_price
    global second_gramm
    global second_price
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("↩️Посчитать еще раз"))
    markup.add(types.KeyboardButton("⭕️Вернуться в главное меню"))
    if message.text == "⭕️Вернуться в главное меню":
        start(message)
        return
    try:
        first_price = float(first_price)
        second_price = float(message.text)
    except:
        bot.send_message(message.chat.id, text='Только цирфы, долбоеб')
        start(message)
    if first_gramm < 10:
        first_gramm = first_gramm * 1000
    if second_gramm < 10:
        second_gramm = second_gramm * 1000
    bot.send_message(message.chat.id, text=makeculc(first_price, second_price, first_gramm, second_gramm),
                     reply_markup=markup)
    # print(f'{first_gramm} за {first_price} и {second_gramm} за {second_price}.')
    # print()


def makeculc(pervoe, vtoroe, pervoegram, vtoroegram):
    try:
        a = pervoe / pervoegram
        b = vtoroe / vtoroegram
        if a < b:
            d = a * 0.33
            if (a + d) < b and b / (a + d) > 1.05:
                c = '%s рублей за %s грамм выгоднее,\nчем %s рублей за %s грамм!\nОчень выгодно!' % (
                    pervoe, pervoegram, vtoroe, vtoroegram)
                e = '1️⃣Первый продукт лучше!'
            else:
                c = '%s рублей за %s грамм выгоднее,\nчем %s рублей за %s грамм!' % (
                    pervoe, pervoegram, vtoroe, vtoroegram)
                e = '1️⃣Первый продукт лучше!'
        elif a == b:
            c = '⏸У них одинаковая цена'
            e = ""
        else:
            d = b * 0.33
            if (b + d) < a and a / (b + d) > 1.05:
                c = '%s рублей за %s грамм выгоднее,\nчем %s рублей за %s грамм!\nОчень выгодно!' % (
                    vtoroe, vtoroegram, pervoe, pervoegram)
                e = '2️⃣Второй продукт лучше!'
            else:
                c = '%s рублей за %s грамм выгоднее,\nчем %s рублей за %s грамм!' % (
                    vtoroe, vtoroegram, pervoe, pervoegram)
                e = '2️⃣Второй продукт лучше!'
        return c +'\n'+ e
    except:
        return 'Ошибка'


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
                """, parse_mode='html', reply_markup=markup)
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
                caseprice = str(cursor.fetchone()[0]) + ' руб.'
                # print(str(cursor.fetchone()[0])+' руб.')
                urltaken = 'Этот кейс уже записан и имеет находится под <b>ID: %s</b> в датабазе\nУстановленная цена:<b>%s</b> Хочешь перезаписать его цену?' % (
                caseid, caseprice)
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
    if message.text == "⭕️Вернуться в главное меню":
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
            cursor.execute("UPDATE cases SET price = ? WHERE url = ? AND userid = ?", [price, url,
                                                                                       message.from_user.id])
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
    if message.text == "⭕️Вернуться в главное меню":
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
        if mainparsing.taketokens(message.from_user.id) == 'Ок':
            bot.reply_to(message, 'Токены добавлены в базу!\nНо ты их не увидишь...', reply_markup=markup)
            start(message)
        else:
            bot.reply_to(message, 'Гдето ты напортачил...', reply_markup=markup)
            myprofile(message)
    elif message.text == '❌ Удалить кейсы':
        caselist = maindatabasecode.deletecase1(message.from_user.id)
        deletecasetext = ''
        for i in range(len(caselist)):
            deletecasetext = deletecasetext + 'ID ' + str(caselist[i][0]) + ': ' + str(caselist[i][1]) + '\n'
        msg = bot.reply_to(message, f'Введите числовой ID кейса, который хотите удалить.\n{deletecasetext}',
                           reply_markup=markup2)
        bot.register_next_step_handler(msg, handler_deletecase)


def handler_deletecase(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("⚪️Вернуться в главное меню"))
    if message.text == "⚪️Вернуться в главное меню":
        start(message)
        return
    try:
        bot.send_message(message.chat.id, text=maindatabasecode.deletecase2(message))
        sleep(0.5)
        myprofile(message)
    except:
        bot.send_message(message.chat.id, text="Ты чото делаешь не так, давай сначала", reply_markup=markup)
        start(message)
        print(traceback.format_exc())


def handler_caselookup(message):
    if message.text == "⭕️Вернуться в главное меню":
        start(message)
        return
    else:
        buttons(message)
        return


if __name__ == '__main__':
    print('  Date         | @username | Message text')
    bot.infinity_polling()

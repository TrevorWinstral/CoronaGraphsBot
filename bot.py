import telebot
from telebot import types
import time
import os
import sys
import logging
import pickle

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)
TOKEN = os.environ['TELEGRAM_TOKEN']

bot = telebot.TeleBot(token=TOKEN)


default_dict = {'Country': 'Switzerland',
                'Days': 0}


with open('settings.pkl', 'rb') as inFile:
    user_dict = pickle.load(inFile)

with open('continents.pkl', 'rb') as inFile:
    country_dict = pickle.load(inFile)


admins = [995547885]
EU = [country for country in country_dict if country_dict[country] == 'EU']
SA = [country for country in country_dict if country_dict[country] == 'SA']
NA = [country for country in country_dict if country_dict[country] == 'NA']
AF = [country for country in country_dict if country_dict[country] == 'AF']
AS = [country for country in country_dict if country_dict[country] == 'AS']
OC = [country for country in country_dict if country_dict[country] == 'OC']
region_dict = {'EU': EU, 'SA': SA, 'NA': NA, 'AF': AF, 'AS': AS, 'OC': OC}
Countries = [country for country in country_dict]


@bot.message_handler(commands=['start'])
def send_welcome(message):
    global user_dict
    chat_id = message.chat.id
    #markup = types.ReplyKeyboardRemove(selective=False)
    try:
        user_dict[message.chat.id]
    except:
        user_dict[message.chat.id] = default_dict
        logger.log(20, msg='New User!')
    bot.reply_to(message, f"Hello, Welcome the the COVID Graphs ChatBot?\nTry /start, /help, or /menu\nCurrent Settings: {user_dict[chat_id]['Country']}, {user_dict[chat_id]['Days']} Days")


@bot.message_handler(commands=['help'])
def help_fct(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, text='For questions, contact Trevor Winstral on Twitter: https://twitter.com/TrevorWinstral\nUse /menu to return')

@bot.message_handler(commands=['menu'])
def menu(message):
    chat_id = message.chat.id
    markup = types.ReplyKeyboardMarkup()
    itembtna = types.KeyboardButton('/help')
    itembtnv = types.KeyboardButton('/GetUpdate')
    itembtnc = types.KeyboardButton('/SetCountry')
    itembtnd = types.KeyboardButton('/SetTimeFrame')
    markup.row(itembtna, itembtnv)
    markup.row(itembtnc, itembtnd)
    bot.send_message(chat_id, text="Menu - Choose an Option:", reply_markup=markup)


@bot.message_handler(commands=['SetCountry'])
def country_select(message):
    chat_id = message.chat.id
    markup = types.ReplyKeyboardMarkup()

    itembtna = types.KeyboardButton('/NA')
    itembtnb = types.KeyboardButton('/SA')
    itembtnc = types.KeyboardButton('/EU')
    itembtnd = types.KeyboardButton('/AF')
    itembtne = types.KeyboardButton('/AS')
    itembtnf = types.KeyboardButton('/OC')
    itembtns = types.KeyboardButton('/start')

    markup.row(itembtna, itembtnb, itembtnc)
    markup.row(itembtnd, itembtne, itembtnf)
    markup.row(itembtns)
    bot.send_message(chat_id, text="Choose a region:", reply_markup=markup)


@bot.message_handler(commands=['EU', 'SA', 'NA', 'AF', 'AS', 'OC'])
def choose_country_in_region(message):
    global user_dict
    chat_id = message.chat.id
    markup = types.ReplyKeyboardMarkup(row_width=3)

    region = region_dict[message.text[1:]]
    for country in region:
        markup.add(types.KeyboardButton(f'/{country}'))

    bot.send_message(chat_id, text="Choose a Country:", reply_markup=markup)


@bot.message_handler(commands=[f'{Country}' for Country in Countries])
def country_set(message):
    global user_dict
    chat_id = message.chat.id

    try:
        user_dict[chat_id]['Country'] = message.text[1:]
    except:
        user_dict[chat_id] = default_dict
        user_dict[chat_id]['Country'] = message.text[1:]

    bot.send_message(
        chat_id, text=f"Country set to {user_dict[chat_id]['Country']}")
    menu(message)


@bot.message_handler(commands=['SetTimeFrame'])
def choose_time_frame(message):
    chat_id = message.chat.id
    markup = types.ReplyKeyboardMarkup(row_width=3)

    markup.add(types.KeyboardButton('/7'))
    markup.add(types.KeyboardButton('/14'))
    markup.add(types.KeyboardButton('/30'))
    markup.add(types.KeyboardButton('/60'))
    markup.add(types.KeyboardButton('/All'))
    markup.add(types.KeyboardButton('/menu'))

    bot.send_message(
        chat_id, text='Time Frame can be set to last 7, 14, 30, 60, or All Days', reply_markup=markup)
    


@bot.message_handler(commands=['7', '14', '30', '60', 'All'])
def set_time_frame(message):
    global user_dict
    chat_id = message.chat.id

    days_dict = {'/7': 7, '/14': 14, '/30': 30, '/60': 60, '/All': 0}

    try:
        user_dict[chat_id]['Days'] = days_dict[message.text]
    except:
        user_dict[chat_id] = default_dict
        user_dict[chat_id]['Days'] = days_dict[message.text]
    bot.send_message(
        chat_id, text=f'Time Frame set to {message.text[1:]} Days')
    menu(message)


@bot.message_handler(commands=['GetUpdate'])
def get_update(message):
    global user_dict
    chat_id = message.chat.id
    graphTypes = ['TotalCases', 'ActiveCases', 'NewCases']
    print(f'A user has requested: {user_dict[chat_id]}')
    imgFiles = [
        f"{user_dict[chat_id]['Country']}_{graph}_{user_dict[chat_id]['Days']}Days.png" for graph in graphTypes]

    for img in imgFiles:
        try:
            photo = open(f'Images/{img}', 'rb')
            bot.send_photo(chat_id, photo)
            photo.close()
        except:
            bot.send_message(chat_id, text=f'No Image found for {img.split("_")[1]}')

    bot.send_message(chat_id, text='/menu /start /help')

@bot.message_handler(commands=['Dump', 'dump'])
def pkl_dump(message):
    global user_dict
    chat_id = message.chat.id
    if chat_id in admins:
        try:
            logger.log(20, msg=f'Total Users: {len(user_dict)}')
            with open('settings.pkl', 'wb') as outFile:
                pickle.dump(user_dict, outFile)
                logger.log(
                    20, msg=f'{time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime())} Dumping User Preferences to pickle')
            bot.send_message(chat_id, text=f'User Settings Dumped, Total Users: {len(user_dict)}')
        except Exception as e:
            bot.send_message(chat_id, text=f'Error:\n{e}')

    else:
        bot.send_message(chat_id, text='Insufficient Permissions')


start = time.time()
while True:
    now = time.time()
    if now-start >= 5*60:  # Update user_dict at most every 5 minutes
        start= now
        logger.log(20, msg=f'Total Users: {len(user_dict)}')
        with open('settings.pkl', 'wb') as outFile:
            pickle.dump(user_dict, outFile)
            logger.log(
                20, msg=f'{time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime())} Dumping User Preferences to pickle')
    try:
        bot.polling(none_stop=False, interval=0, timeout=1)
    except Exception as e:
        print(e)
        time.sleep(15)

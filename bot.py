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
                'Days': 0,
                'Subscribed':False}


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

START = time.time()

briefing() #Run the Briefing

def time_check(force=False):
    global START
    diff = time.time() - START
    if diff >= (60*10) or force=True:  # update at most every 10 minutes or when forced
        logger.log(20, msg=f'Total Users: {len(user_dict)}')
        with open('settings.pkl', 'wb') as outFile:
            pickle.dump(user_dict, outFile)
            logger.log(
                20, msg=f'{time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime())} Dumping User Preferences to pickle')
        START = time.time()
    return


@bot.message_handler(commands=['start', 'Start'])
def send_welcome(message):
    global user_dict
    chat_id = message.chat.id
    #markup = types.ReplyKeyboardRemove(selective=False)
    try:
        user_dict[message.chat.id]
    except:
        user_dict[message.chat.id] = default_dict
        logger.log(20, msg='New User!')
    bot.reply_to(message, f"Hello, Welcome the COVID Graphs ChatBot!\nTry /start, /help, /ExplainData. /menu will allow you to set your country and get updated! If you don't see a menu come up after that, click on the square icon in the message field.\nCurrent Settings: {user_dict[chat_id]['Country']}, {user_dict[chat_id]['Days']} Days")


@bot.message_handler(commands=['help'])
def help_fct(message):
    chat_id = message.chat.id
    bot.send_message(
        chat_id, text='For questions, contact Trevor Winstral on Twitter: https://twitter.com/TrevorWinstral')
    bot.send_message(chat_id, text='/start /menu /ExplainData')


@bot.message_handler(commands=['ExplainData'])
def explain_data(message):
    chat_id = message.chat.id
    bot.send_message(chat_id,
                     """
Data is from John Hopkins University: https://github.com/datasets/covid-19, and is updated once every day

Active Cases is the sum of the last 7 days of new cases, and is only an estimate.

You can view the Source Code at: https://github.com/TrevorWinstral/CoronaGraphsBot

For more questions see /help
    """)
    bot.send_message(chat_id, text="/menu /start /help")


@bot.message_handler(commands=['thanks'])
def thank(message):
    chat_id = message.chat.id
    bot.send_message(
        chat_id, text="A big thank you to Vitek and Pavel for their help in testing, looking at my code, and making feature reccomendations! Also thank you to Sebastien for hosting the bot on his server!")


@bot.message_handler(commands=['menu', 'Menu'])
def menu(message):
    chat_id = message.chat.id
    markup = types.ReplyKeyboardMarkup()
    itembtna = types.KeyboardButton('/help')
    itembtnv = types.KeyboardButton('/GetUpdate')
    itembtnc = types.KeyboardButton('/SetCountry')
    itembtnd = types.KeyboardButton('/SetTimeFrame')
    markup.row(itembtna, itembtnv)
    markup.row(itembtnc, itembtnd)
    bot.send_message(chat_id, text="/Menu - Choose an Option:",
                     reply_markup=markup)


@bot.message_handler(commands=['SetCountry'])
def country_select(message):
    chat_id = message.chat.id
    markup = types.ReplyKeyboardMarkup()

    bot.send_message(chat_id, text=f"To go back use /menu")

    itembtna = types.KeyboardButton('/NA')
    itembtnb = types.KeyboardButton('/SA')
    itembtnc = types.KeyboardButton('/EU')
    itembtnd = types.KeyboardButton('/AF')
    itembtne = types.KeyboardButton('/AS')
    itembtnf = types.KeyboardButton('/OC')
    itembtns = types.KeyboardButton('/Menu')

    markup.row(itembtna, itembtnb, itembtnc)
    markup.row(itembtnd, itembtne, itembtnf)
    markup.row(itembtns)
    bot.send_message(chat_id, text="Choose a region:", reply_markup=markup)


@bot.message_handler(commands=['EU', 'SA', 'NA', 'AF', 'AS', 'OC'])
def choose_country_in_region(message):
    global user_dict
    chat_id = message.chat.id

    bot.send_message(chat_id, text=f"To go back use /menu")
    markup = types.ReplyKeyboardMarkup(row_width=3)

    region = region_dict[message.text[1:]]
    for country in region:
        markup.add(types.KeyboardButton(f"/{country.replace(' ', '_')}"))

    bot.send_message(chat_id, text="Choose a Country:", reply_markup=markup)


@bot.message_handler(commands=[f'{Country.replace(" ", "_")}' for Country in Countries])
def country_set(message):
    global user_dict
    chat_id = message.chat.id

    try:
        user_dict[chat_id]['Country'] = message.text[1:].replace('_', ' ')
    except:
        user_dict[chat_id] = default_dict
        user_dict[chat_id]['Country'] = message.text[1:].replace('_', ' ')

    bot.send_message(
        chat_id, text=f"Country set to {user_dict[chat_id]['Country']}")

    time_check(force=True)
    menu(message)


@bot.message_handler(commands=['SetTimeFrame'])
def choose_time_frame(message):
    chat_id = message.chat.id
    markup = types.ReplyKeyboardMarkup(row_width=3)

    markup.add(types.KeyboardButton('/14'))
    markup.add(types.KeyboardButton('/30'))
    markup.add(types.KeyboardButton('/60'))
    markup.add(types.KeyboardButton('/All'))
    markup.add(types.KeyboardButton('/menu'))

    bot.send_message(
        chat_id, text='Time Frame can be set to last 14, 30, 60, or All Days', reply_markup=markup)


@bot.message_handler(commands=['14', '30', '60', 'All'])
def set_time_frame(message):
    global user_dict
    chat_id = message.chat.id

    days_dict = {'/14': 14, '/30': 30, '/60': 60, '/All': 0}

    try:
        user_dict[chat_id]['Days'] = days_dict[message.text]
    except:
        user_dict[chat_id] = default_dict
        user_dict[chat_id]['Days'] = days_dict[message.text]
    bot.send_message(
        chat_id, text=f'Time Frame set to {message.text[1:]} Days')

    time_check(force=True)
    menu(message)


@bot.message_handler(commands=['GetUpdate'])
def get_update(message):
    global user_dict
    chat_id = message.chat.id
    graphTypes = ['Deaths', 'TotalCases', 'ActiveCases', 'NewCases']
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

            if chat_id in admins:
                bot.send_message(chat_id, text=f'File: {img}')

    bot.send_message(chat_id, text='/menu /start /help /GetTheNumbers')


@bot.message_handler(commands=['GetTheNumbers'])
def serve_the_numbers(message):
    chat_id = message.chat.id

    try:
        photo = open(f"Images/{user_dict[chat_id]['Country']}_RawTable.png", 'rb')
        bot.send_photo(chat_id, photo)
        photo.close()
    except:
        bot.send_message(chat_id, text=f'No Image found for {user_dict[chat_id]["Country"]} RawTable')

        if chat_id in admins:
            bot.send_message(chat_id, text=f"File: Images/{user_dict[chat_id]['Country']}_RawTable.png")

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


def briefing():
    global user_dict
    global admins

    for user in user_dict:
        try:
            if user_dict[user][Subscribed] == True:
            chat_id = user
            graphTypes = ['Deaths', 'TotalCases', 'ActiveCases', 'NewCases']
            imgFiles = [
                f"{user_dict[chat_id]['Country']}_{graph}_{user_dict[chat_id]['Days']}Days.png" for graph in graphTypes]

            for img in imgFiles:
                try:
                    photo = open(f'Images/{img}', 'rb')
                    bot.send_photo(chat_id, photo)
                    photo.close()
                except:
                    bot.send_message(chat_id, text=f'No Image found for {img.split("_")[1]}')

                    if chat_id in admins:
                        bot.send_message(chat_id, text=f'File: {img}')
                try:
                    photo = open(f"Images/{user_dict[chat_id]['Country']}_RawTable.png", 'rb')
                    bot.send_photo(chat_id, photo)
                    photo.close()
                except:
                    bot.send_message(chat_id, text=f'No Image found for {user_dict[chat_id]["Country"]} RawTable')

                    if chat_id in admins:
                        bot.send_message(chat_id, text=f"File: Images/{user_dict[chat_id]['Country']}_RawTable.png")


            bot.send_message(chat_id, text='This has been your daily briefing, to unsubscribe use /Unsub')
                
        except:
            user_dict[user][Subscribed] = False


    return


@bot.message_handler(commands=['Unsub', 'Unsubscribe'])
def unsubscribe(message):
    global user_dict
    chat_id = message.chat.id
    user_dict[chat_id][Subscribed] = False
    bot.send_message(chat_id, text='You have unsubscribed from your daily briefing.')
    time_check(force=True)
    menu(message)
    return

@bot.message_handler(commands=['Sub', 'Subscribe'])
def subscribe(message):
    global user_dict
    chat_id = message.chat.id
    user_dict[chat_id][Subscribed] = True
    bot.send_message(chat_id, text='You have successfully subscribed to be daily briefed')
    time_check(force=True)
    menu(message)
    return

while True:
    try:
        bot.polling(none_stop=False, interval=0, timeout=5)
    except Exception as e:
        print(e)
        bot.stop_polling()
        time.sleep(5)

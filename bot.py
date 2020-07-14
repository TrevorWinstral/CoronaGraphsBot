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
                'Subscribed':True}


with open('settings.pkl', 'rb') as inFile:
    user_dict = pickle.load(inFile)

with open('continents.pkl', 'rb') as inFile:
    country_dict = pickle.load(inFile)


admins = [995547885, 1043935476]
EU = [country for country in country_dict if country_dict[country] == 'EU']
SA = [country for country in country_dict if country_dict[country] == 'SA']
NA = [country for country in country_dict if country_dict[country] == 'NA']
AF = [country for country in country_dict if country_dict[country] == 'AF']
AS = [country for country in country_dict if country_dict[country] == 'AS']
OC = [country for country in country_dict if country_dict[country] == 'OC']
region_dict = {'EU': EU, 'SA': SA, 'NA': NA, 'AF': AF, 'AS': AS, 'OC': OC}
Countries = [country for country in country_dict]

START = time.time()


def time_check(force=False):
    global START
    global user_dict
    diff = time.time() - START
    if diff >= (60*10) or force==True:  # update at most every 10 minutes or when forced
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
    bot.reply_to(message, f"Hello, Welcome the COVID Graphs ChatBot!\nTry /Tutorial or /help for assistance using the bot. Daily Briefings are default, to turn these off use /Unsub, otherwise check out /GetUpdate to get an update right now!\n/menu will allow you to set your country and get updated! If you don't see a menu come up after that, click on the square icon in the message field.\nCurrent Settings: {user_dict[chat_id]['Country']}, {user_dict[chat_id]['Days']} Days")


@bot.message_handler(commands=['help'])
def help_fct(message):
    chat_id = message.chat.id
    bot.send_message(chat_id,
        text="""Commands:
/start presents the welcome message
/help gives you an overview of the commands,  who to contact, and links to the tutorial
/Tutorial gives a more in depth tutorial for using the bot
/ExplainData tells you about the data used to create these figures
/menu pops out the menu
/SetCountry allows you to set your country to get information on (you must choose your continent first)
/SetTimeFrame allows you to set what time frame you would like to be presented
/GetTheNumbers gets you the raw data for the last few days
/Subscribe subscribes you to the daily briefing
/Unsubscribe unsubscribes you from the daily briefing
        """)
    bot.send_message(
        chat_id, text='If a menu is not popping up after using /menu, try clicking the rounded square in the message field. For an in depth tutorial of the bot, use /Tutorial.\nFor questions, contact Trevor Winstral on Twitter: https://twitter.com/TrevorWinstral')
    bot.send_message(chat_id, text='/start /menu /ExplainData')


@bot.message_handler(commands=['Tutorial', 'tutorial'])
def tutorial(message):
    chat_id = message.chat.id
    bot.send_message(chat_id,
        text="""
Welcome to the Tutorial for using this bot. The basis for using everything is the menu which can be accessed at any time by typing /menu or clicking on /menu here. 
If the a menu does not appear on the bottom of your screen you may have to click on the rounded square (with 4 smaller squares inside) in the message input field at the bottom of your screen.
Once you have opened the menu you have 4 options: /USAGraphs, /GetUpdate, /SetCountry, and /SetTimeFrame.
/USAGraphs (not added yet) gets you access to figures from ECV (endcoronavirus.org) pertaining to the United States.
/GetUpdate serves you an update with you current settings which you can adjust with the following 2 settings.
/SetCountry allows you to choose your country (choose your continent first NA = North America, AS = Asia, etc) and this can be changed at any time by invoking /SetCountry or using the menu option.
/SetTimeFrame allows you to select what time period you would like to see. The numbers refer to the last X days (/14 gives you the last 14 days) and /All gives you the entire Time Frame (starts in early February 2020).

Furthermore, there is a daily briefing feature, to receive your preset settings every day use /Sub to subscribe, and to stop use /Unsub. For any further questions, please feel free to contact me via Twitter: twitter.com/TrevorWinstral
    """)
    bot.send_message(chat_id, text='/start /menu /ExplainData')
    menu(message)  


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
    markup.add(types.KeyboardButton('/90'))
    markup.add(types.KeyboardButton('/All'))
    markup.add(types.KeyboardButton('/menu'))

    bot.send_message(
        chat_id, text='Time Frame can be set to last 14, 30, 60, or All Days', reply_markup=markup)


@bot.message_handler(commands=['14', '30', '60','90', 'All'])
def set_time_frame(message):
    global user_dict
    chat_id = message.chat.id

    days_dict = {'/14': 14, '/30': 30, '/60': 60, '/90':90, '/All': 0}

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
    logger.log(20, f'A user ({chat_id}) has requested: {user_dict[chat_id]}')
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
        bot.send_message(admins[0], f'chat id: {chat_id}')
        bot.send_message(chat_id, text='Insufficient Permissions')


def briefing():
    global user_dict
    global admins

    for user in user_dict:
        try:
            if user_dict[user]['Subscribed'] == True:
                chat_id = user
                graphTypes = ['Deaths', 'TotalCases', 'ActiveCases', 'NewCases']
                imgFiles = [
                    f"{user_dict[chat_id]['Country']}_{graph}_{user_dict[chat_id]['Days']}Days.png" for graph in graphTypes]
                
                try:
                    photo = open(f"Images/{user_dict[chat_id]['Country']}_RawTable.png", 'rb')
                    bot.send_photo(chat_id, photo)
                    photo.close()
                except:
                    bot.send_message(chat_id, text=f'No Image found for {user_dict[chat_id]["Country"]} RawTable')

                    if chat_id in admins:
                        bot.send_message(chat_id, text=f"File: Images/{user_dict[chat_id]['Country']}_RawTable.png")

                for img in imgFiles:
                    try:
                        photo = open(f'Images/{img}', 'rb')
                        bot.send_photo(chat_id, photo)
                        photo.close()
                    except:
                        bot.send_message(chat_id, text=f'No Image found for {img.split("_")[1]}')

                        if chat_id in admins:
                            bot.send_message(chat_id, text=f'File: {img}')
                

                bot.send_message(chat_id, text='This has been your daily briefing. To unsubscribe use /Unsub')
                
        except:
            user_dict[user]['Subscribed'] = False


    return


@bot.message_handler(commands=['Unsub', 'Unsubscribe'])
def unsubscribe(message):
    global user_dict
    chat_id = message.chat.id
    user_dict[chat_id]['Subscribed'] = False
    bot.send_message(chat_id, text='You have unsubscribed from your daily briefing. To subscribe use /Sub')
    time_check(force=True)
    menu(message)
    return

@bot.message_handler(commands=['Sub', 'Subscribe'])
def subscribe(message):
    global user_dict
    chat_id = message.chat.id
    user_dict[chat_id]['Subscribed'] = True
    bot.send_message(chat_id, text='You have successfully subscribed to be daily briefed. To unsubscribe use /Unsub')
    time_check(force=True)
    menu(message)
    return


@bot.message_handler(commands=['SendAll'])
def SendIt(message):
    msg = message.text.replace('/SendAll ', '')
    if message.chat.id in admins:
        for user in user_dict:
            time.sleep(2)
            bot.send_message(user, text=msg)


#briefing() #Run the Briefing

while True:
    try:
        bot.polling(none_stop=False, interval=0, timeout=5)
    except Exception as e:
        print(e)
        bot.stop_polling()
        time.sleep(5)

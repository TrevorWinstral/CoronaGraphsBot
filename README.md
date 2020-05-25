# CoronaGraphsBot
A Telegram Bot to deliver current graphical representations of SARS-CoV-2 outbreak. Check it out here: http://t.me/CovidGraph_bot

# Functionality
Every day country data is retrieved retrieved from https://github.com/datasets/covid-19 (get_data.py), data is then assimilated into graphs (generate_plots.py and plot_data.py). These serve as a basis for the chatbot (bot.py) to serve the information to users. User preferences are stored in the settings pickle. This is currently running on my Raspberry Pi.

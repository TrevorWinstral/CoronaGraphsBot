import os
import pickle

with open('continents.pkl','rb') as inFile:
    countries = pickle.load(inFile)

os.system('python get_data.py')

Days = [0, 14, 30, 60]
for country in countries:
    for days in Days:
        print(f'Creating {country} {days} Days')
        os.system(f'python -W ignore plot_data.py {country.replace(" ", "_")} {days}')
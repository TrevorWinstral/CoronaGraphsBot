import os
import pickle
os.nice(1)
rel_path = '/'.join(os.path.abspath(__file__).split('/')[:-1])
# print(rel_path)

with open('continents.pkl', 'rb') as inFile:
    countries = pickle.load(inFile)

os.system(f'python3 {os.path.join(rel_path, "get_data.py")}')

Days = [0, 14, 30, 60]
while True:
    for country in countries:
        for days in Days:
            print(f'Creating {country} {days} Days')
            os.system(f'python3 -W ignore {os.path.join(rel_path, "plot_data.py")} {country.replace(" ", "_")} {days}')

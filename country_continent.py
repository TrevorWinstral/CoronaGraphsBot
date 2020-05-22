import pycountry_convert as pcc
import pandas as pd 
import numpy as np
import pickle

PKL_FILE = 'continents.pkl'
CSV = 'Countries.csv'

name_dict = {'Burma':'Myanmar',
            'US': 'USA'}
def correct_name(name):
    if name in name_dict:
        return name_dict[name]
    return name

def convert(name):
    try:
        x = pcc.country_alpha2_to_continent_code(pcc.country_name_to_country_alpha2(correct_name(name)))
    except:
        x = None
    return x

def main():
    df = pd.read_csv(CSV)
    df.drop('Unnamed: 0', 1, inplace=True)
    countries = np.array(df.loc[:,'0'])
    continent_dict = {x:convert(x) for x in countries if convert(x) != None}

    with open(PKL_FILE, 'wb') as outFile:
        pickle.dump(continent_dict, outFile)

if __name__ == "__main__":
    main()

'''
with open('continents.pkl', 'rb') as inFile:
    a = pickle.load(inFile)
'''
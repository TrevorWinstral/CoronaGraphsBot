import pandas as pd
import os

URL = 'https://raw.github.com/datasets/covid-19/master/data/countries-aggregated.csv'
URL = 'https://raw.github.com/TrevorWinstral/COVID_simplified/master/countries-aggregated..csv'
rel_path = '/'.join(os.path.abspath(__file__).split('/')[:-1])
out_file = os.path.join(rel_path, 'data.csv')
print(out_file)

def main():
    try:
        data = pd.read_csv(URL, quotechar='"')
        data.to_csv(out_file)
        print('Data Retrieved\n')
    except Exception as e:
        print(f'URL: {URL}\n{e}\n\n')
    return


if __name__ == "__main__":
    main()

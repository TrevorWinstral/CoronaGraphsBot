import pandas as pd

URL = 'https://raw.github.com/datasets/covid-19/master/data/countries-aggregated.csv'


def main():
    try:
        data = pd.read_csv(URL, quotechar='"')
        data.to_csv('data.csv')
        print('Data Retrieved\n')
    except Exception as e:
        print(f'URL: {URL}\n{e}\n\n')
    return


if __name__ == "__main__":
    main()

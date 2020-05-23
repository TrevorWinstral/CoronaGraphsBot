import csv
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
from sys import argv
plt.style.use('ggplot')

DATA_FILE= 'data.csv'

def main():
    try:
        COUNTRY = argv[1].replace("_", " ")
        LAST_DAYS = int(argv[2])
    except:
        COUNTRY = 'Switzerland'
        LAST_DAYS = 0

    data = pd.read_csv(DATA_FILE, quotechar='"')
    data.drop('Unnamed: 0', 1, inplace=True)

    country = data[data['Country'] == COUNTRY]
    country.loc[:,'New'] = country.loc[:,'Confirmed'].diff()
    country.loc[:,'7-Day'] = country.loc[:,'New'].rolling(5).mean()
    country.loc[:,'Active 7 Day'] = country.loc[:,'New'].rolling(7).sum()
    #print(country.tail(5))

    def get_ticks(steps, xlim):
        xmin, xmax = xlim
        locs, stepsize = np.linspace(xmin, xmax, steps, retstep=True)
        stepsize = int(np.floor(stepsize))
        if stepsize==0:
            stepsize = 1
        ticks = country['Date'][::stepsize]
        return(locs, ticks)

    quick_dict = {0: 'All', 14:'Last 14', 30:'Last 30', 60:'Last 60'} # mostly just to convert 0 days to all days in title

    country = country.iloc[-1*LAST_DAYS:]

    steps = 15

    # New Cases Per Day
    plt.scatter(country['Date'], country['New'], s=3)
    plt.plot(country['Date'], country['New'], linewidth=0.5, label='New Cases Per Day')
    plt.plot(country['Date'], country['7-Day'], linewidth=2, label='7 Day Rolling Average', c='green')
    
    current = country['7-Day'].iloc[-1]
    plt.plot(country['Date'], [current for i in country['7-Day']], linestyle='--', c='orange', label='Current Level')

    locs, labels = get_ticks(steps, plt.xlim())
    plt.xticks(locs, labels, rotation=70)
    plt.legend()
    plt.title(f'New Cases ({quick_dict[LAST_DAYS]} Days) - {COUNTRY}')
    plt.tight_layout()
    plt.savefig(f'Images/{COUNTRY}_NewCases_{LAST_DAYS}Days')
    #plt.show()
    plt.clf()

    # Active Cases
    plt.plot(country['Date'], country['Active 7 Day'], label='Active Cases (7 Day)')
    current = country['Active 7 Day'].iloc[-1]
    plt.plot(country['Date'], [current for i in country['Active 7 Day']], linestyle='--', label='Current Level')

    locs, labels = get_ticks(steps, plt.xlim())
    plt.xticks(locs, labels, rotation=70)
    plt.title(f'Active Cases ({quick_dict[LAST_DAYS]} Days) - {COUNTRY}')
    plt.legend()
    plt.tight_layout()
    plt.savefig(f'Images/{COUNTRY}_ActiveCases_{LAST_DAYS}Days')
    #plt.show()    
    plt.clf()

    
    # Total Cases
    fig, ax = plt.subplots()
    ax.semilogy(country['Date'], country['Confirmed'], label='Total Cases')
    ax.semilogy(country['Date'], country['Recovered'], label='Recovered', c='green')
    
    ax.grid(b=True, which='major', axis='both')
    locs, labels = get_ticks(steps, plt.xlim())
    ax.set_xticks(locs)
    ax.set_xticklabels(labels, rotation=70)
    plt.title(f'Total Cases ({quick_dict[LAST_DAYS]} Days) (Logarithmic) - {COUNTRY}')
    ax.legend(loc='upper left')

    '''
    ax2 = ax.twinx()
    ax2.semilogy(country['Date'], country['Deaths'], label='Deaths', c='black')
    ax2.legend(loc='lower right')
    #ax2.yaxis.set_minor_formatter(mticker.ScalarFormatter())
    ax2.set_ylabel('Deaths')
    '''

    plt.tight_layout()
    plt.savefig(f'Images/{COUNTRY}_TotalCases_{LAST_DAYS}Days')
    #plt.show()
    plt.clf()

    # Deaths
    fig, ax = plt.subplots()
    ax.semilogy(country['Date'], country['Deaths'], label='Deaths', c='black')
    ax.grid(b=True, which='major', axis='both')

    locs, labels = get_ticks(steps, plt.xlim())
    ax.set_xticks(locs)
    ax.set_xticklabels(labels, rotation=70)
    plt.title(f'Total Deaths ({quick_dict[LAST_DAYS]} Days) (Logarithmic) - {COUNTRY}')
    #ax2.yaxis.set_minor_formatter(mticker.ScalarFormatter())
    ax.legend()
    plt.tight_layout()
    plt.savefig(f'Images/{COUNTRY}_Deaths_{LAST_DAYS}Days')
    #plt.show()
    plt.clf()

    return

if __name__ == "__main__":
    main()
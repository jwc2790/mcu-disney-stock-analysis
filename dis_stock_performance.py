"""
@author Joe Cuffney <josephcuffney@gmail.com>
"""
import datetime

import matplotlib.pyplot as plt  # plot library
import pandas as pd  # python data analysis toolkit

"""
plots the stock data as a movie is released and saves it to the results folder.
"""


def create_plot(data, title='', save=False):
    fig = plt.figure()
    plt.plot(data.index, data['adj_close'])
    plt.ylabel('price')
    plt.xlabel('date')
    # rotate the x axis so that the dates fit better
    plt.xticks(rotation=45)
    plt.title(title)
    if save:
        fig.subplots_adjust(bottom=0.3)
        # str interpolation
        fig.savefig(f'./results/{title}.png')
    else:
        plt.show()


"""
looks in the historical stock data and pulls out the range of prices before and after the movie release
"""


def lookup_dis_price(df, start, end):
    return df.loc[start:end]


"""
reads in historical stock data, as well as mcu movie release data
loops over the movie releases and looks up the stock data before and after the movie release
generate a graph with the following data points:
    - adjusted close price
"""


def main():
    # DIS data
    dis_dtypes = {'date': 'str', 'open': 'float', 'high': 'float', 'low': 'float', 'adj_close': 'float',
                  'volume': 'float'}
    dis_parse_dates = ['date']
    dis_data_frame = pd.read_csv('./data/DIS.csv', sep=',', dtype=dis_dtypes, parse_dates=dis_parse_dates)
    dis_data_frame = dis_data_frame.set_index(['date'])

    # MCU data
    mcu_dtypes = {'title': 'str', 'adjusted_gross': 'float', 'unadjusted_gross': 'float', 'release_date': 'str'}
    mcu_parse_dates = ['release_date']
    mcu_data_frame = pd.read_csv('./data/MCU.csv', sep=',', dtype=mcu_dtypes, parse_dates=mcu_parse_dates)

    for movie in mcu_data_frame.itertuples():
        delta = datetime.timedelta(days=10)
        movie_release_date = movie[4]
        start = movie_release_date - delta
        end = movie_release_date + delta
        data = lookup_dis_price(dis_data_frame, start, end)
        create_plot(data, movie[1], True)


if __name__ == "__main__":
    main()

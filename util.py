"""Utility functions"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import time
import urllib

def portfolio_statistics(df, print_stats = False):
    """Get portfolio statistics

    Parameters
    ----------
    df: data frame with portfolio data

    Returns a list containing Cumulative return, Average daily return, Risk (std of daily return), Sharpe Ratio
    """

    # Compute data by symbol
    daily_returns = compute_daily_returns(df)

    # Debug
    plot_data(daily_returns, title = 'Daily returns', xlabel = 'Date', ylabel = '..')

    # Sum by column (by symbol)
    allsymbols_daily_returns = daily_returns.sum(axis = 1)

    # Average return
    avg_daily_returns = allsymbols_daily_returns.mean()

    # Risk
    risk = allsymbols_daily_returns.std()
    
    #avg_daily_returns = np.mean(daily_returns)
    #risks = daily_returns.sum(axis = 1).std()

    if print_stats == True:
        print "Cumulative return: {}".format(allsymbols_daily_returns.sum())
        print "Average daily return: {}".format(avg_daily_returns)
        print "Risk: {}".format(risk)
        print "Sharpe Ratio: {}".format(sharpe_ratio(daily_returns))

def select_portfolio(symbols, start_date, stats_dates, ref_symbol, skip_download = False):
    """Download and preprocess a list of symbols

    Parameters
    ----------
    symbols: list of symbols to consider
    start_date: start date used to download data
    stats_dates: dates range used to build statistics, in the form ['2009-01-01','2009-12-31']
    ref_symbol: market reference

    Returns ...
    """

    # Use always the reference symbol also
    symbols.append(ref_symbol)

    # Download data
    if skip_download == False:
        try:
            download_data(symbols, start_date)
        except:
            print "Unable to download selected data, processing old files on disk."

    # Build dataframes
    curr_date = datetime.now()
    #dates = pd.date_range(start_date, "{}-{}-{}".format(curr_date.year, curr_date.month, curr_date.day))
    dates = pd.date_range(stats_dates[0], stats_dates[1])
    df = get_data(symbols, dates, ref_symbol)

    # Fill missing values
    fill_missing_values(df)

    # Plot
    plot_data(df)

    # Compute statistics
    portfolio_statistics(df, True)
    
def plot_selected(df, columns, start_index, end_index):
    """Plot the desired columns over index values in the given range."""
    df_temp = df.ix[start_index : end_index, columns]
    plot_data(df_temp, "Selected data")

def download_data(symbols, from_date):
    """Download the desired symbol data from specified date to today, with a daily basis."""
    curr_date = datetime.now()
    from_date = datetime.strptime(from_date, '%Y-%m-%d')
    for symbol in symbols:
	link = "http://chart.finance.yahoo.com/table.csv?s={}&a={}&b={}&c={}&d={}&e={}&f={}&g=d&ignore=.csv".format(
            symbol, from_date.month - 1, from_date.day, from_date.year, curr_date.month - 1, curr_date.day, curr_date.year)
	file_name = "data\{}.csv".format(symbol)
        print "Downloading {}...".format(file_name)
	urllib.urlretrieve(link, file_name)

def symbol_to_path(symbol, base_dir = "data"):
    """Return CSV file path given ticker symbol."""
    return os.path.join(base_dir, "{}.csv".format(str(symbol)))

def get_data(symbols, dates, ref_symbol = 'SPY'):
    """Read stock data (adjusted close) for given symbols from CSV files."""
    df = pd.DataFrame(index = dates)
    if ref_symbol not in symbols: # add ref_symbol(SPY) for reference, if absent
        symbols.insert(0, ref_symbol)
    
    for symbol in symbols:
        df_temp = pd.read_csv(symbol_to_path(symbol), index_col = "Date",
                        parse_dates = True, usecols = ['Date', 'Adj Close'], 
                        na_values = ['nan'])
        # Rename to prevent clash
        df_temp = df_temp.rename(columns = {'Adj Close' : symbol})
        df = df.join(df_temp)
        if symbol == ref_symbol: # drop dates ref_symbol(SPY) did not trade
            df = df.dropna(subset = [ref_symbol])
        
    return df
    
def plot_data(df, title = 'Stock Prices', xlabel = 'Date', ylabel = 'Price'):
    '''Plot stock prices'''
    axis = df.plot(title = title, fontsize = 12)
    axis.set_xlabel(xlabel)
    axis.set_ylabel(ylabel)
    plt.show()

def how_long(func, *args):
    """Execute function with given arguments, measurng exec time."""
    t0 = time()
    result = func(*args)
    t1 = time()
    return result, t1 - t0

def get_rolling_mean(values, window):
    """Return rolling mean of given values, using specified window size."""
    return pd.rolling_mean(values, window=window)

def get_rolling_std(values, window):
    """Return rolling standard deviation of given values, using specified window size."""
    return pd.rolling_std(values, window = window)

def get_bollinger_bands(rm, rstd):
    """Return upper and lower Bollinger Bands."""
    upper_band = rm + 2 * rstd
    lower_band = rm - 2 * rstd
    return upper_band, lower_band

def compute_daily_returns(df):
    """Compute and return the daily return values."""
    daily_returns = (df / df.shift(1)) - 1 # with Pandas
    daily_returns.ix[0, :] = 0 # set daily returns for row 0 to 0
    return daily_returns

def fill_missing_values(df_data):
    """Fill missing values in data frame, in place."""
    df_data.fillna(method="ffill", inplace=True)
    df_data.fillna(method="bfill", inplace=True)

def sharpe_ratio(daily_returns, daily_rf = 0):
    """SR = mean(daily_rets - daily_rf) / std(daily_rets - daily_rf)

    Daily_rf can be computed in three ways:
    * LIBOR
    * 3mo T-bill
    * 0% (present positive interest of a bank)"""
    daily_returns = daily_returns - daily_rf
    daily_returns = daily_returns.sum(axis = 1)
    sr = daily_returns.mean() / daily_returns.std()
    return sr * np.sqrt(252)
    

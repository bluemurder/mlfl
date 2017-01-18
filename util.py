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
    print_stats: flag used to print evaluated data

    Returns a list containing Cumulative return, Average daily return, Risk (std of daily return), Sharpe Ratio
    """

    # Compute data by symbol
    daily_returns = compute_daily_returns(df)

    # Debug
    plot_data(daily_returns, title = 'Daily returns', xlabel = 'Date', ylabel = '..')

    # Sum by column (by symbol)
    allsymbols_daily_returns = daily_returns.sum(axis = 1)

    # Cumulative return
    cumulative_return = allsymbols_daily_returns.sum()

    # Average return
    avg_daily_return = allsymbols_daily_returns.mean()

    # Risk
    risk = allsymbols_daily_returns.std()

    # Sharpe ratio
    sharpe_ratio_annualized = sharpe_ratio(daily_returns)

    if print_stats == True:
        print "Cumulative return: {}".format(cumulative_return)
        print "Average daily return: {}".format(avg_daily_return)
        print "Risk: {}".format(risk)
        print "Sharpe Ratio: {}".format(sharpe_ratio_annualized)

    return (cumulative_return, avg_daily_return, risk, sharpe_ratio_annualized)

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
    #symbols.append(ref_symbol)

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

    # Select one stock
    df = pd.DataFrame(df['ANX.MI'])

    plot_data(df)

    # Compute momentum
    #m = momentum(df, 15)

    # Compute SMA
    sma = simple_moving_average(df, 15)

    # Compute bollinger bands
    ubb, lbb = bollinger_bands(df, 15)

    # Join momentum on the same plot
    #df = df.join(m)

    # Join SMA on same plot
    sma = pd.DataFrame(sma)
    sma.columns = ["ANX.MI_SMA_15"]
    df = df.join(sma)

    # Join BB on same plot
    ubb = pd.DataFrame(ubb)
    ubb.columns = ["ANX.MI_upperBB_15"]
    lbb = pd.DataFrame(lbb)
    lbb.columns = ["ANX.MI_lowerBB_15"]
    df = df.join(ubb)
    df = df.join(lbb)

    plot_data(df)
    
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

    # Add ref_symbol(default: SPY) for reference, if absent
    if ref_symbol not in symbols: 
        symbols.insert(0, ref_symbol)
    
    for symbol in symbols:
        df_temp = pd.read_csv(symbol_to_path(symbol), index_col = "Date",
                        parse_dates = True, usecols = ['Date', 'Adj Close'], 
                        na_values = ['nan'])

        # Rename column name
        df_temp = df_temp.rename(columns = {'Adj Close' : symbol})
        df = df.join(df_temp)

        # Drop dates ref_symbol(default: SPY) did not trade
        if symbol == ref_symbol: 
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
    # deprecated return pd.rolling_mean(values, window=window)
    return values.rolling(window = window, center = False).mean()

def get_rolling_std(values, window):
    """Return rolling standard deviation of given values, using specified window size."""
    # deprecated return pd.rolling_std(values, window = window)
    return values.rolling(window = window, center = False).std()

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

def momentum(df, n = 5, print_stats = False):
    """Evaluates momentum with a look of n-th value in the past.
    Momentum[t] = price[t] / price[t-n] -1

    Parameters
    ----------
    df: dataframe containing symbols data
    n: the shift in the past to consider

    Returns a dataframe with momentum data for each stock
    """

    # Evaluate momentum
    momentum_by_stock = (df / df.shift(n)) - 1

    # Set to zero first values to erase NaN entries
    momentum_by_stock.ix[0 : n, :] = 0

    # Print if requested
    if print_stats == True:
        print "momentum:\n{}".format(momentum_by_stock)

    symbols = list(momentum_by_stock.columns.values)
    column_names = []
    for symbol in symbols:
        column_names.append(symbol + "_Momentum_" + str(n))

    momentum_by_stock.columns = column_names
    
    return momentum_by_stock

def simple_moving_average(df, n):
    """Simple Moving Average for given stocks"""
    return get_rolling_mean(df, n)

def bollinger_bands(df, n):
    """Bollinger Bands for given stocks"""
    rolling_mean = get_rolling_mean(df, n)
    rolling_std = get_rolling_std(df, n)
    return get_bollinger_bands(rolling_mean, rolling_std)

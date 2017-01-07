"""Utility functions"""

import os
import pandas as pd
import matplotlib.pyplot as plt

def plot_selected(df, columns, start_index, end_index):
    """Plot the desired columns over index values in the given range."""
    df_temp = df.ix[start_index : end_index, columns]
    plot_data(df_temp, "Selected data")

def symbol_to_path(symbol, base_dir = "data"):
    """Return CSV file path given ticker symbol."""
    return os.path.join(base_dir, "{}.csv".format(str(symbol)))

def get_data(symbols, dates):
    """Read stock data (adjusted close) for given symbols from CSV files."""
    df = pd.DataFrame(index = dates)
    if 'SPY' not in symbols: # add SPY for reference, if absent
        symbols.insert(0, 'SPY')
    
    for symbol in symbols:
        df_temp = pd.read_csv(symbol_to_path(symbol), index_col = "Date",
                        parse_dates = True, usecols = ['Date', 'Adj Close'], 
                        na_values = ['nan'])
        # Rename to prevent clash
        df_temp = df_temp.rename(columns = {'Adj Close' : symbol})
        df = df.join(df_temp)
        if symbol == 'SPY': # drop dates SPY did not trade
            df = df.dropna(subset = ["SPY"])
        
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


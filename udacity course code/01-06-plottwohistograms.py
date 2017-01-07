"""Plot a couple of histogram."""

import pandas as pd
import matplotlib.pyplot as plt
from util import get_data, plot_data, compute_daily_returns

def test_run():
    # Read data
    dates = pd.date_range('2009-01-01', '2012-12-31')  # date range as index
    symbols = ['SPY','XOM']
    df = get_data(symbols, dates)  # get data for each symbol
    #plot_data(df)

    # Compute daily returns
    daily_returns = compute_daily_returns(df)
    #plot_data(daily_returns, title = "Daily returns", ylabel = "Daily returns")

    # Compute and plot a couple of histograms on same chart
    daily_returns['SPY'].hist(bins = 20, label = 'SPY')
    daily_returns['XOM'].hist(bins = 20, label = 'XOM')
    plt.legend(loc = 'upper right')
    plt.show()

if __name__ == "__main__":
    test_run()

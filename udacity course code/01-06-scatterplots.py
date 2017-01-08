"""Scatterplots."""

import pandas as pd
import matplotlib.pyplot as plt
from util import get_data, plot_data, compute_daily_returns
import numpy as np

def test_run():
    # Read data
    dates = pd.date_range('2009-01-01', '2012-12-31')  # date range as index
    symbols = ['SPY','XOM','GLD']
    df = get_data(symbols, dates)  # get data for each symbol
    plot_data(df)

    # Compute daily returns
    daily_returns = compute_daily_returns(df)
    plot_data(daily_returns, title = "Daily returns", ylabel = "Daily returns")

    # Scatterplots SPY versus XOM
    daily_returns.plot(kind = 'scatter', x = 'SPY', y = 'XOM')
    beta_XOM, alpha_XOM = np.polyfit(daily_returns['SPY'], daily_returns['XOM'], 1)
    print "beta_XOM=", beta_XOM
    print "alpha_XOM=", alpha_XOM
    plt.plot(daily_returns['SPY'], beta_XOM * daily_returns['SPY'] + alpha_XOM, '-', color = 'r')
    plt.show()

    # Scatterplots SPY versus GLD
    daily_returns.plot(kind = 'scatter', x = 'SPY', y = 'GLD')
    beta_GLD, alpha_GLD = np.polyfit(daily_returns['SPY'], daily_returns['GLD'], 1)
    print "beta_GLD=", beta_GLD
    print "alpha_GLD=", alpha_GLD
    plt.plot(daily_returns['SPY'], beta_GLD * daily_returns['SPY'] + alpha_GLD, '-', color = 'r')
    plt.show()

    # Comment: beta_XOM is fairly high than beta_GLD, so XOM is more reactive
    # to the market than GLD.

    # On the other hand, alpha values denote how well the products performs well
    # with respect to SPY. In this case, alpha_XOM is negative, and alpha_GLD is
    # positive. This means that GLD performs better.

    # Calculate correlation coefficient
    print daily_returns.corr(method = 'pearson')

    # As you have seen in this lesson, the distribution of daily returns for
    # stocks and the market look very similar to a Gaussian.
    # This property persists when we look at weekly, monthly, and annual returns
    # as well.
    # If they were really Gaussian we'd say the returns were normally distributed.
    # In many cases in financial research we assume the returns are normally distributed.
    # But this can be dangerous because it ignores kurtosis or the probability
    # in the tails.
    # In the early 2000s investment banks built bonds based on mortgages.
    # They assumed that the distribution of returns for these mortgages was
    # normally distributed.
    # On thet basis they were able to show that these bonds had a very low probability of default.
    # But they made two mistakes. First, they assumed that the return of each
    # of these mortgages was independent; and two that this return would be
    # normally distributed.
    # Both of these assumptions proved to be wrong, as massive number of omeowners
    # defaulted on their mortgages.
    # It was these defaults that precipitated the great recession of 2008.
    # 

if __name__ == "__main__":
    test_run()

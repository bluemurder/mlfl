"""Utility functions"""

import os
import pandas as pd
import matplotlib.pyplot as plt

def plot_selected(df, columns, start_index, end_index):
    """Plot the desired columns over index values in the given range."""
    # TODO: Your code here
    # Note: DO NOT modify anything else!
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
	
def plot_data(df, title = 'Stock Prices'):
	'''Plot stock prices'''
	axis = df.plot(title = title, fontsize = 12)
	axis.set_xlabel("Date")
	axis.set_ylabel("Price")
	plt.show()
	
def test_run():
	# Define a data range
	dates = pd.date_range('2010-01-01', '2010-12-31')
	
	# Choose stock symbols to read
	symbols = ['GOOG', 'IBM', 'GLD'] # SPY will be added in get_data()
	
	# Get stock data
	df = get_data(symbols, dates)
	#print df
	
	# Slice by row range (dates) using DataFrame.ix[] selector
	print df.ix['2010-01-01' : '2010-01-31']
	
	# Slice by columns (symbols)
	print df.['GOOG']
	print df[['IBM', 'GLD']]
	
	# Slice by row and columns
	print df.ix['2010-01-01' : '2010-01-31', ['SPY', 'IBM']]
	
if __name__ == "__main__":
    test_run()

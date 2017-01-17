import util
import config
import time
from datetime import datetime

def test_run():
    print "Welcome to MLFL {}".format(config.version)
    print "Start date: {}".format(config.start_date)
    print ""
    print "Select action:"
    print "1. Select portfolio"
    print "0. Exit"

    choice = '1' #raw_input()

    if choice == '1':
        symbol_list = config.test_portfolio #raw_input("Insert symbol list comma separated\n")
        symbol_list.append('ANX.MI')
        symbols = symbol_list #symbol_list.upper().split(',')
        if len(symbols) < 1:
            print "Error, symbol list not valid"
            exit()
        util.select_portfolio(symbols, config.start_date, ['2015-01-01', '2015-12-31'], config.ref_symbol, skip_download = True)
        #util.select_portfolio(symbols, config.start_date, ['2009-01-01', '2017-01-15'], config.ref_symbol, skip_download = True)
        
    elif choice == '0':
        print "Exiting..."
        exit()
    else:
        print "Invalid choice"
        exit()

if __name__ == "__main__":
    test_run()

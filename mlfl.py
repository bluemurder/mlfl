import util
import config

def test_run():
    print "Welcome to MLFL {}".format(config.version)
    print "Start date: {}".format(config.start_date)
    print ""
    print "Select action:"
    print "1. Select portfolio"
    print "0. Exit"

    choice = raw_input()

    if choice == '1':
        symbol_list = raw_input("Insert symbol list comma separated\n")
        select_portfolio(symbol_list)
        
    elif choice == '0':
        print "Exiting..."
        exit()
    else:
        print "Invalid choice"
        exit()

def select_portfolio(symbols_comma_separated):
    """Download and preprocess a list of symbols"""
    symbols = symbols_comma_separated.upper().split(',')
    if len(symbols) < 1:
        print "Error, symbol list not valid"
        return

    # Use always the reference symbol also
    symbols.append(config.ref_symbol)

    # Download data
    util.download_data(symbols, config.start_date)

    

if __name__ == "__main__":
    test_run()

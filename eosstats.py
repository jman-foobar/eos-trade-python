from eoslist import *
from coinmarket import EOSMarket
import pprint
import numpy

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class EOSStats():

    def __init__(self, offline=False, verbose=True):
        if offline == True:
            self.el = EOSOffLineList() # reads local json file
        else:
            print "Retrieving coinmarketcap.com json data..."
            self.el = EOSOnLineList() # downloads json from https://eos.io
        if verbose == True:
            self.print_eos_list()

        if offline == False:
            print "Retrieving coinmarketcap.com json data..."
            self.eos_market = EOSMarket()
            if verbose == True:
                self.print_eos_price()

        if verbose == True:
            self.print_eos_stats()

    def print_eos_list(self):
        print """
        *** EOS Data***
        """
        pprint.pprint(self.el.eos_list)

    def print_eos_price(self):
        print """
        *** LIVE EOS PRICE on CoinMarket Cap ***
        """
        self.eos_market = EOSMarket()
        print "Price USD: \033[92m%s\033[0m" % (self.eos_market.get_value('price_usd'))
        print "Price BTC: \033[92m%s\033[0m" % (self.eos_market.get_value('price_btc'))

    def print_eos_stats(self):
        print """
        **** 200,000,000 & 2,000,000 STATISTICS ***
        """
        print "Average ETH per ICO: \033[93m%f ETH\033[0m" % (self.avg_eth())
        print "Median ETH per ICO: \033[93m%f ETH\033[0m" % (self.median_eth())
        print
        print "Average value of EOS per ICO: \033[93m%f BTC\033[0m" % (self.avg_price())
        print "Median value of EOS per ICO: \033[93m%f BTC\033[0m" % (self.median_price())
        print
        print "Hightest ETH Total: \033[93m%f ETH\033[0m" % (self.highest_eth())
        print "Lowest ETH Total: \033[93m%f ETH\033[0m" % (self.lowest_eth())
        print
        print "Highest BTC: \033[93m%f BTC\033[0m" % (self.highest_price())
        print "Lowest BTC: \033[93m%f BTC\033[0m" % (self.lowest_price())
        print
        print "Average EOS for 1 ETH: \033[94m%f EOS\033[0m" % (self.avg_eos())
        print "Median EOS for 1 ETH: \033[94m%f EOS\033[0m" % (self.median_eos())
        print "Highest EOS for 1 ETH: \033[94m%f EOS\033[0m" % (self.highest_eos())
        print "Lowest EOS for 1 ETH: \033[94m%f EOS\033[0m" % (self.lowest_eos())
        print
        print """
        **** 2,000,000 STATISTICS ***
        """
        print "Daily Average ETH per 2,000,000 ICO: \033[93m%f ETH\033[0m" % (self.daily_avg_eth())
        print "Daily Median ETH per 2,000,000 ICO: \033[93m%f ETH\033[0m" % (self.daily_median_eth())
        print
        print "Daily Average value of EOS per 2,000,000 ICO: \033[93m%f BTC\033[0m" % (self.daily_avg_price())
        print "Daily Median value of EOS per 2,000,000 ICO: \033[93m%f BTC\033[0m" % (self.daily_median_price())
        print
        print "Daily Hightest ETH Total: \033[93m%f ETH\033[0m" % (self.daily_highest_eth())
        print "Daily Lowest ETH Total: \033[93m%f ETH\033[0m" % (self.daily_lowest_eth())
        print
        print "Daily Highest BTC: \033[93m%f BTC\033[0m" % (self.daily_highest_price())
        print "Daily Lowest BTC: \033[93m%f BTC\033[0m" % (self.daily_lowest_price())
        print
        print "Daily Average EOS for 1 ETH: \033[94m%f EOS\033[0m" % (self.daily_avg_eos())
        print "Daily Median EOS for 1 ETH: \033[94m%f EOS\033[0m" % (self.daily_median_eos())
        print "Daily Highest EOS for 1 ETH: \033[94m%f EOS\033[0m" % (self.daily_highest_eos())
        print "Daily Lowest EOS for 1 ETH: \033[94m%f EOS\033[0m" % (self.daily_lowest_eos())
        print

        print """
        **** TODAY'S ICO ***
        """
        print "Total ETH submitted so far: \033[95m%s ETH \033[0m(Better to be low)" % (self.todays_eth())
        print "Today's BTC value: \033[95m%s BTC \033[0m(Better to be high)" % (self.todays_price())
        print "Today's EOS for 1 ETH: \033[95m%s EOS \033[0m(Best to be high)" % (self.todays_eos())
        print "Time Remaining: \033[95m%s \033[0m(Best if 30 min remaining)" % (self.time_left())

    """
    Daily average value in ETH per 2,000,000 ICO
    """
    def daily_avg_eos(self):
        return numpy.mean(self.el.eos_formula_values(1,-1))

    """
    Daily Average ETH per 2,000,000 ICO
    Total Eth / Total Days
    """
    def daily_avg_eth(self):
        return numpy.average(self.el.eth_values(1,-1)) # first sale ran for 5 days and skews results. last sale ongoing.

    """
    Daily Average value of EOS per 2,000,000 ICO in BTC
    Daily Value / Total Days
    """
    def daily_avg_price(self):
        return numpy.average(self.el.eos_values(1,-1)) # first sale ran for 5 days and skews results. last sale ongoing.

    """
    Highest ETH per 2,000,000 ICO
    """
    def daily_highest_eth(self):
        return numpy.amax(self.el.eth_values(1,-1)) # first sale ran for 5 days and skews results. last sale ongoing.

    """
    Lowest ETH per 2,000,000 ICO
    """
    def daily_lowest_eth(self):
        return numpy.amin(self.el.eth_values(1,-1)) # first sale ran for 5 days and skews results. last sale ongoing.

    """
    Highest BTC per 2,000,000 ICO
    """
    def daily_highest_price(self):
        return numpy.amax(self.el.eos_values(1,-1)) # first sale ran for 5 days and skews results. last sale ongoing.

    """
    Lowest BTC per 2,000,000 ICO
    """
    def daily_lowest_price(self):
        return numpy.amin(self.el.eos_values(1,-1)) # first sale ran for 5 days and skews results. last sale ongoing.

    """
    Daily Median ETH of EOS per 2,000,000 ICO
    """
    def daily_median_eth(self):
        return numpy.median(self.el.eth_values(1,-1)) # first sale ran for 5 days and skews results. last sale ongoing.

    """
    Daily Median value of EOS per 2,000,000 ICO in BTC
    """
    def daily_median_price(self):
        return numpy.median(self.el.eos_values(1,-1)) # first sale ran for 5 days and skews results. last sale ongoing.

    """
    Daily average value in ETH per 2,000,000 ICO
    """
    def daily_avg_eos(self):
        return numpy.average(self.el.eos_formula_values(1,-1))

    """
    Daily average value in ETH per 2,000,000 ICO
    """
    def daily_median_eos(self):
        return numpy.median(self.el.eos_formula_values(1,-1))

    """
    Daily highest value in ETH per 2,000,000 ICO
    """
    def daily_highest_eos(self):
        return numpy.amax(self.el.eos_formula_values(1,-1))

    """
    Daily lowest valuye in ETH per 2,000,000 ICO
    """
    def daily_lowest_eos(self):
        return numpy.amin(self.el.eos_formula_values(1,-1))


    """
    INCLUDE ALL ICO'S
    """

    """
    Total average value in ETH per ICO
    """
    def avg_eos(self):
        return numpy.mean(self.el.eos_formula_values())

    """
    Average ETH per ICO
    Total Eth / Total Days
    """
    def avg_eth(self):
        return numpy.average(self.el.eth_values(0,-1)) # last sale ongoing.

    """
    Daily Average value of EOS per ICO in BTC
    Daily Value / Total Days
    """
    def avg_price(self):
        return numpy.average(self.el.eos_values(0,-1)) # last sale ongoing.

    """
    Highest ETH per ICO
    """
    def highest_eth(self):
        return numpy.amax(self.el.eth_values(0,-1)) # last sale ongoing.

    """
    Lowest ETH per ICO
    """
    def lowest_eth(self):
        return numpy.amin(self.el.eth_values(0,-1)) # last sale ongoing.

    """
    Highest BTC per ICO
    """
    def highest_price(self):
        return numpy.amax(self.el.eos_values(0,-1)) # last sale ongoing.

    """
    Lowest BTC per ICO
    """
    def lowest_price(self):
        return numpy.amin(self.el.eos_values(0,-1)) # last sale ongoing.

    """
    Median ETH of EOS per ICO
    """
    def median_eth(self):
        return numpy.median(self.el.eth_values(0,-1)) # last sale ongoing.

    """
    Median value of EOS per ICO in BTC
    """
    def median_price(self):
        return numpy.median(self.el.eos_values(0,-1)) # first sale ran for 5 days and skews results. last sale ongoing.

    """
    Average value in ETH per ICO
    """
    def avg_eos(self):
        return numpy.average(self.el.eos_formula_values(0,-1))

    """
    Average value in ETH per ICO
    """
    def median_eos(self):
        return numpy.median(self.el.eos_formula_values(0,-1))

    """
    Highest value in ETH per ICO
    """
    def highest_eos(self):
        return numpy.amax(self.el.eos_formula_values(0,-1))

    """
    lowest value in ETH per ICO
    """
    def lowest_eos(self):
        return numpy.amin(self.el.eos_formula_values(0,-1))


    """
    Today's Values
    """
    def todays_eth(self):
        return self.el.eth_values(-1, self.el.length()) # Last in list is today.

    def todays_price(self):
        return self.el.eos_values(-1, self.el.length())

    def todays_eos(self):
        return self.el.eos_formula_values(-1, self.el.length())

    def time_left(self):
        return self.el.time_left(-1)


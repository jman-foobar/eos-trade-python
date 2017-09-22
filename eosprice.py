import urllib2
import sys
import re

class PriceError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

"""
Retrieve the current EOS price from Bitmex in BTC.
Potential to add more sites in future by updating static dictionaries
"""
class EOSPrice():

    url = { 'Bitmex':'https://www.bitmex.com/app/trade/EOSN17' }
    pattern = { 'Bitmex': '[0-9]\.[0-9][0.9][0-9][0-9][0-9][0-9] \(EOSN17\)' } #e.g., 0.001013 (EOSN17)

    def __init__(self, key='Bitmex'):
        self.price = self.__matchprice__(self.__getsite__(key), key)

    def __getsite__(self, site_key):
        try:
            print "Retrieving EOS Price from %s ..." % (site_key)
            return urllib2.urlopen(EOSPrice.url[site_key]).read() # returns exchange website
        except urllib2.HTTPError, e:
            print('HTTPError = ' + str(e.code))
        except urllib2.URLError, e:
            print('URLError = ' + str(e.reason))
        except Exception:
            print "Unexpected error:", sys.exc_info()[0]
            raise

    """
    Returns a floating number of the price of EOS in Bitcoin
    """
    def __matchprice__(self, site_page, pattern_key='Bitmex'):
        print "Matching EOS RegEx for  %s" % (pattern_key)
        eospricematch = re.search(EOSPrice.pattern[pattern_key], site_page)
        if eospricematch:
            eosprice = eospricematch.group().split()[0]
            return float(eosprice)
        else:
            raise PriceError("Could not match %s price" % (pattern_key))

    def __str__(self):
        return "EOS Price: %f BTC" % (self.price)


def test():
    price = EOSPrice()
    print price

test()

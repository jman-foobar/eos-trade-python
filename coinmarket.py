import urllib2
import sys
import json

"""
From http://coinmarketcap.com/api/
"""

class CoinMarket():

    url = 'https://api.coinmarketcap.com/v1/ticker/'

    def __init__(self, coincode=''):
        self.json_data = json.loads((self.__getsite__(CoinMarket.url+coincode)))


    def __getsite__(self, url):
        try:
            return urllib2.urlopen(url).read()
        except urllib2.HTTPError, e:
            print('HTTPError = ' + str(e.code))
        except urllib2.URLError, e:
            print('URLError = ' + str(e.reason))
        except Exception:
            print "Unexpected error:", sys.exc_info()[0]
            raise

"""
[
    {
        "id": "eos",
        "name": "EOS",
        "symbol": "EOS",
        "rank": "13",
        "price_usd": "1.21075",
        "price_btc": "0.00064164",
        "24h_volume_usd": "31288900.0",
        "market_cap_usd": "268655397.0",
        "available_supply": "221891718.0",
        "total_supply": "1000000000.0",
        "percent_change_1h": "-1.01",
        "percent_change_24h": "-11.2",
        "percent_change_7d": "-47.64",
        "last_updated": "1500242056"
    }
]
"""
class EOSMarket(CoinMarket):

    def __init__(self, coincode='EOS'):
        CoinMarket.__init__(self, coincode)

    def get_value(self, key):
        return self.json_data[0][key]

    def __str__(self):
        return "***JSON FILE***\n%s" % (self.json_data)

"""
def test():
    eos = EOSMarket()
    print eos
    print "Price USD: %s" % (eos.get_value('price_usd'))

test()
"""

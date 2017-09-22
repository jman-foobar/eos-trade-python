import eosico
import json
from datetime import datetime, tzinfo,timedelta
import pytz
import urllib2
import sys

#UTC to Korean
class UTC(tzinfo):

    def utcoffset(self, dt):
        return timedelta(hours=-9)

    def dst(self, dt):
        return timedelta(0)

class EosIcoList():

    def __init__(self, url='https://eos.io/eos-sales-statistic.php'):
        self.eos_list = []
        json_file = json.loads(self.__geturl__(url))
        self.__buildlist__(json_file)

    def __geturl__(self, url):
        try:
            return urllib2.urlopen(url).read() # returns json
        except urllib2.HTTPError, e:
                print('HTTPError = ' + str(e.code))
        except urllib2.URLError, e:
                print('URLError = ' + str(e.reason))
        except Exception:
            print "Unexpected error:", sys.exc_info()[0]
            raise

    """
    build the list of EOS ICO json data from start date up to present day ico only
    """
    def __buildlist__(self, json_file):
        count = 1
        for ico in json_file:
            if count == 1: # first line is different as it was the 200,000,000 EOS
                sale_id = int(ico['id'])
                start_datetime = datetime.strptime("2017-06-26T13:00:00", "%Y-%m-%dT%H:%M:%S") #manually insert 5-day ico
                end_datetime, tz = ico['ends'].split('.')
                end_datetime = datetime.strptime(end_datetime, "%Y-%m-%dT%H:%M:%S")
                eth_sold = float(ico['dailyTotal'])
                eos_bought = int(ico['createOnDay'])
                eos = eosico.EosIco(sale_id, start_datetime, end_datetime, eth_sold, eos_bought)
            else: # all other lines sell 2,000,000 EOS
                sale_id = int(ico['id'])
                start_datetime, tz = ico['begins'].split('.')
                start_datetime = datetime.strptime(start_datetime, "%Y-%m-%dT%H:%M:%S")
                end_datetime, tz = ico['ends'].split('.')
                end_datetime = datetime.strptime(end_datetime, "%Y-%m-%dT%H:%M:%S")
                eth_sold = float(ico['dailyTotal'])
                eos_bought = int(ico['createOnDay'])
            if pytz.utc.localize(end_datetime) > datetime.now(UTC()): #cannot compare naive to aware. use pytz to make it aware.
                break #ico data is for future ico so break from loop
            else:
                eos = eosico.EosIco(sale_id, start_datetime, end_datetime, eth_sold, eos_bought)
                self.eos_list.append(eos)
                count += 1

"""
def test():
    eos_list = EosIcoList()
    print eos_list.eos_list

test()
"""

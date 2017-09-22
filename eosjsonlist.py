
import eosico
import json
from datetime import datetime, date, tzinfo, timedelta
import pytz
import numpy as np

#Eastern Std Time
class EST(tzinfo):

    def utcoffset(self, dt):
        return timedelta(hours=-5)

    def dst(self, dt):
        return timedelta(0)


#Korean Std Time
class KST(tzinfo):

    def utcoffset(self, dt):
        return timedelta(hours=+9)

    def dst(self, dt):
        return timedelta(0)

#UTC to Korean
class UTC(tzinfo):

    def utcoffset(self, dt):
        return timedelta(hours=-9)

    def dst(self, dt):
        return timedelta(0)

class EOSJsonList():

    def __init__(self):
        self.eos_list = []
        with open('eos-sales-statistic.json', 'r') as f:
            data = json.load(f)
            count = 1
            for ico in data:
                if count == 1: # first line is different as it was the 200,000,000 EOS with no start date
                    sale_id = int(ico['id'])
                    eos_created_on_day = int(ico['createOnDay'])
                    daily_total_eth = float(ico['dailyTotal'])
                    price = float(ico['price'])
                    begins = datetime.strptime("2017-06-26T13:00:00", "%Y-%m-%dT%H:%M:%S") #manually insert 5-day ico
                    end_datetime, tz = ico['ends'].split('.')
                    ends = datetime.strptime(end_datetime, "%Y-%m-%dT%H:%M:%S")

                else: # all other lines sell 2,000,000 EOS
                    sale_id = int(ico['id'])
                    eos_created_on_day = int(ico['createOnDay'])
                    daily_total_eth = float(ico['dailyTotal'])
                    price = float(ico['price'])
                    start_datetime, tz = ico['begins'].split('.')
                    begins = datetime.strptime(start_datetime, "%Y-%m-%dT%H:%M:%S")
                    end_datetime, tz = ico['ends'].split('.')
                    ends = datetime.strptime(end_datetime, "%Y-%m-%dT%H:%M:%S")

                if pytz.utc.localize(begins) > datetime.now(UTC()): #cannot compare naive to aware. use pytz to make it aware.
                    break #ico data is for future ico so break from loop
                else:
                    eos = eosico.EosIco(sale_id, eos_created_on_day, daily_total_eth, price, begins, ends)
                    self.eos_list.append(eos)
                    count += 1

    """
    Return the length of the list
    """
    def length(self):
        return len(self.eos_list)

    """
    Return the List of populated EOS objects
    """
    def list(self, start=None, end=None):
        if start == None:
            start = 0
        if end == None:
            end = len(self.eos_list)
        return self.eos_list[start:end]

    """
    Return datetime.timedelta(days, seconds, microseconds) of the ico in the list
    """
    def time_left(self, position):
        ends = self.eos_list[position].ends
        return (pytz.utc.localize(ends) - datetime.now(UTC()))


    """
    Return an array of the EOS ICO daily sales in ETH
    start: index to list
    end: index to list
    """
    def eth_values(self, start, end):
        a = []
        for i in self.eos_list[start:end]:
            a.append(i.daily_total_eth)
        return a

    """
    Return an array of the EOS ICO daily prices in BTC
    start: index to list
    end: index to list
    """
    def eos_values(self, start, end):
        a = []
        for i in self.eos_list[start:end]:
            a.append(i.price)
        return a

    """
    Return an array of the EOS ICO daily prices to ETH
    start: index to list
    end: index to list
    """
    def eos_formula_values(self, start, end):
        a = []
        for i in self.eos_list[start:end]:
            a.append(i.eos_formula())
        return a


import eosico
import json
from datetime import datetime, date, tzinfo, timedelta
import pytz

#Eastern Std Time
class EST(tzinfo):

    def utcoffset(self, dt):
        return timedelta(hours=-5)

    def dst(self, dt):
        return timedelta(0)

print datetime.now(EST())

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

print datetime.now(UTC())

eoslist = []
with open('eos-sales-statistic.json', 'r') as f:
    data = json.load(f)
    count = 1
    for ico in data:
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
            eos = eosico.EosIco(sale_id, start_datetime, end_datetime, eth_sold, eos_bought)
        eoslist.append(eos)
        count += 1
for i in eoslist:
    if pytz.utc.localize(i.end_datetime) > datetime.now(UTC()): #cannot compare naive to aware. use pytz to make it aware.
        break #ico data is for future ico so break from loop
    print i
    print "1 ETH: %f" % (i.eos_formula(1, i.eos_bought, i.eth_sold))


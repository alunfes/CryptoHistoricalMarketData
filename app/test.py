from typing import Any


import pandas as pd
import requests
import yaml
import asyncio
import aiohttp
import asyncio
import time
import datetime
import sys
from dateutil.parser import isoparse

class test:
    def __init__(self):
        pass


    def dydx(self, symbol):
        since_ts = (int(time.time()) - 60 * 1440 * 10) * 1000
        since_ts = since_ts/1000
        since_ts_iso = datetime.datetime.utcfromtimestamp(int(since_ts)).isoformat()

        # Using direct HTTP API calls for dYdX v4
        market = f"{symbol.upper()}-USD"
        base_url = "https://indexer.dydx.trade/v4/candles/perpetualMarkets"

        while True:
            url = f"{base_url}/{market}"
            params = {
                'resolution': '1MIN',
                'fromISO': since_ts_iso,
            }
            response = requests.get(url, params=params)
            data = response.json()
            
            if 'candles' in data and len(data['candles']) > 0:
                print(since_ts_iso)
                since_ts = int(isoparse(data['candles'][0]['startedAt']).timestamp()) + 1
                since_ts_iso = datetime.datetime.utcfromtimestamp(since_ts).isoformat()
                print(data['candles'][0]['startedAt'], data['candles'][-1]['startedAt'])
                print(since_ts_iso)
            else:
                break
            

if __name__ == '__main__':
    t = test()
    t.dydx('ETH')

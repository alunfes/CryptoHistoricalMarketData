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
from dydx3 import Client
from dydx3.helpers.request_helpers import generate_now_iso
from web3 import Web3
from dydx3.constants import *

class test:
    def __init__(self):
        pass


    def dydx(self, symbol):
        since_ts = (int(time.time()) - 60 * 1440 * 10) * 1000
        since_ts = since_ts/1000
        since_ts_iso = datetime.datetime.utcfromtimestamp(int(since_ts)).isoformat()
        to_ts_iso = 

        client = Client(
            host='https://api.dydx.exchange',
        )
        client.public.get_markets()
        market_symbol = f"MARKET_{symbol.upper()}_USD"

        # getattrを使用して定数の値を取得します
        market = getattr(sys.modules['dydx3.constants'], market_symbol)

        while True:
            candles = client.public.get_candles(
                market=market,
                resolution='1MIN',
                from_iso = since_ts_iso,
            )
            if len(candles.data['candles']) > 0:
                print(since_ts_iso)
                since_ts = int(isoparse(candles.data['candles'][0]['startedAt']).timestamp()) + 1
                since_ts_iso = datetime.datetime.utcfromtimestamp(since_ts).isoformat()
                print(candles.data['candles'][0]['startedAt'], candles.data['candles'][-1]['startedAt'])
                print(since_ts_iso)
            else:
                break
            

if __name__ == '__main__':
    t = test()
    t.dydx('ETH')

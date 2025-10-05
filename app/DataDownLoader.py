'''
/usr/local/lib/python3.11/site-packages/parsimonious/expressions.pyのfrom inspect import getargspecをgetfullargspecに修正

'''

import requests
import yaml
import asyncio
import aiohttp
import asyncio
import time
import datetime
import sys
from dateutil.parser import isoparse



from TickerConverter import TickerConverter
from TickerData import TickerData
from OhlcConverter import OHLCConverter
from OHLCData import OHLCData
from DataWriter import DataWriter


class DataDownLoader:
    def __init__(self) -> None:
        self.exhanges = []
        self.ohlcv_data_interval = {}
        self.since_num_days_before = 0 #days
        self.max_download_per_trial = {}        
        self.ticker_endpoints = {}
        self.ohlc_endpoints = {}
        self.ohlcv_download_num = {}
        self.__read_params()
        self.__read_apiendpoints()
        TickerData.initialize()
        TickerConverter.initialize()
        OHLCConverter.initialize()
        OHLCData.initialize()
        

    def __read_params(self):
        with open('./ignore/params.yaml', 'r') as f:
            params = yaml.load(f, Loader=yaml.FullLoader)
            self.exhanges = params['exchanges']
            self.since_num_days_before = params['since_num_days_before']
            for ex in self.exhanges:
                self.ohlcv_data_interval[ex] = params['ohlcv_data_interval'][ex]
                self.max_download_per_trial[ex] = params['max_download_per_trial'][ex]

    def __read_apiendpoints(self):
        self.api_key = ''
        with open('./ignore/apiendpoints.yaml', 'r') as f:
            endpoints = yaml.load(f, Loader=yaml.FullLoader)
            for ex in self.exhanges:
                self.ticker_endpoints[ex] = endpoints[ex]['ticker']
                self.ohlc_endpoints[ex] = endpoints[ex]['ohlc']


    async def start(self):
        print('Downloading target tickers...')
        await self.__get_tickers()
        await DataWriter.write_ticker_data(self.exhanges)
        print('Started ohlc download process..')
        since_ts = (int(time.time()) - 60 * 1440 * self.since_num_days_before) * 1000
        till_ts = int(time.time()) * 1000
        print('num since ts=', (int(time.time()) - since_ts / 1000) / 60)
        try:
            async with asyncio.TaskGroup() as tg:
                task_okx = tg.create_task(self.__start_okx_ohlcv_download(since_ts, till_ts))
                task_bybit = tg.create_task(self.__start_bybit_ohlcv_download(since_ts, till_ts))
                task_dydx = tg.create_task(self.__start_dydx_ohlcv_download(since_ts, till_ts))
                task_apexpro = tg.create_task(self.__start_apexpro_ohlcv_download(since_ts, till_ts))
        except* Exception as err:
            print(f"{err.exceptions=}")
        print('Completed download all symbol data.')


    async def __start_okx_ohlcv_download(self, since_ts, till_ts):
        tickers = TickerData.get_tickers_by_exchange('okx')
        for ticker in tickers:
            # Check if data already exists and get last timestamp
            last_ts = DataWriter.get_last_timestamp('okx', ticker.base, ticker.quote)
            download_since = last_ts + 60000 if last_ts is not None else since_ts  # Add 1 minute (60000 ms) to avoid duplicate
            
            # Skip if no new data to download
            if download_since >= till_ts:
                print(f'Skipping okx-{ticker.symbol}: data is up to date')
                continue
            
            await self.__download_okx_ohlcv(ticker.symbol, ticker.base, ticker.quote, download_since, till_ts, self.ohlcv_data_interval['okx'])
            await asyncio.sleep(0.5)


    async def __start_bybit_ohlcv_download(self, since_ts, till_ts):
        tickers = TickerData.get_tickers_by_exchange('bybit')
        for ticker in tickers:
            # Check if data already exists and get last timestamp
            last_ts = DataWriter.get_last_timestamp('bybit', ticker.base, ticker.quote)
            download_since = last_ts + 60000 if last_ts is not None else since_ts  # Add 1 minute (60000 ms) to avoid duplicate
            
            # Skip if no new data to download
            if download_since >= till_ts:
                print(f'Skipping bybit-{ticker.symbol}: data is up to date')
                continue
            
            await self.__download_bybit_ohlcv(ticker.symbol, ticker.base, ticker.quote, download_since, till_ts, self.ohlcv_data_interval['bybit'])
            await asyncio.sleep(0.5)

    async def __start_dydx_ohlcv_download(self, since_ts, till_ts):
        tickers = TickerData.get_tickers_by_exchange('dydx')
        for ticker in tickers:
            # Check if data already exists and get last timestamp
            last_ts = DataWriter.get_last_timestamp('dydx', ticker.base, ticker.quote)
            download_since = last_ts + 60000 if last_ts is not None else since_ts  # Add 1 minute (60000 ms) to avoid duplicate
            
            # Skip if no new data to download
            if download_since >= till_ts:
                print(f'Skipping dydx-{ticker.symbol}: data is up to date')
                continue
            
            await self.__download_dydx_ohlcv(ticker.symbol, ticker.base, ticker.quote, download_since, till_ts, self.ohlcv_data_interval['dydx'])
            await asyncio.sleep(0.5)

    async def __start_apexpro_ohlcv_download(self, since_ts, till_ts):
        tickers = TickerData.get_tickers_by_exchange('apexpro')
        for ticker in tickers:
            # Check if data already exists and get last timestamp
            last_ts = DataWriter.get_last_timestamp('apexpro', ticker.base, ticker.quote)
            download_since = last_ts + 60000 if last_ts is not None else since_ts  # Add 1 minute (60000 ms) to avoid duplicate
            
            # Skip if no new data to download
            if download_since >= till_ts:
                print(f'Skipping apexpro-{ticker.symbol}: data is up to date')
                continue
            
            await self.__download_apexpro_ohlcv(ticker.symbol, ticker.base, ticker.quote, download_since, till_ts, self.ohlcv_data_interval['apexpro'])
            await asyncio.sleep(0.01)

    async def __download_okx_ohlcv(self, symbol, base, quote, since_ts, till_ts, bar_size):
        ohlcv = []
        async with aiohttp.ClientSession() as session:
            while True:
                params = {
                    'instId':symbol,
                    'after':till_ts,
                    'bar': bar_size,
                }
                async with session.get(url=self.ohlc_endpoints['okx'], params=params) as resp:
                    res = await resp.json()
                    if 'data' in list(res.keys()):
                        ohlcv.extend(res['data'])
                        if len(res['data']) < 0.5 * self.max_download_per_trial['okx']:
                            break
                        elif since_ts >= till_ts:
                            break
                        else:
                            till_ts = int(res['data'][-1][0])
                    else:
                        print('OKX downloaded ohlc data is not expected format!')
                        print(res)
                        break
                await asyncio.sleep(0.1)
            if len(ohlcv) > 0:
                mode = 'Updated' if DataWriter.file_exists('okx', base, quote) else 'Downloaded'
                print(f'{mode} okx-{symbol} ({base}-{quote}): {len(ohlcv)} records')
                await OHLCConverter.convert_ohlc('okx', ohlcv, symbol, base, quote)
                await DataWriter.write_data('okx', symbol, base, quote)
            else:
                print(f'No new data for okx-{symbol}')



    
    async def __download_bybit_ohlcv(self, symbol, base, quote, since_ts, till_ts, interval):
        ohlcv = []
        async with aiohttp.ClientSession() as session:
            while True:
                params = {
                    'symbol':symbol,
                    'start':since_ts,
                    'interval': interval,
                }
                async with session.get(url=self.ohlc_endpoints['bybit'], params=params) as resp:
                    res = await resp.json()
                    if res['retMsg'] == 'OK':
                        ohlcv.extend(reversed(res['result']['list']))
                        if len(res['result']['list']) < 0.5 * self.max_download_per_trial['bybit']:
                            break
                        elif  int(res['result']['list'][0][0]) >= till_ts:
                            break
                        else:
                            since_ts = int(res['result']['list'][0][0]) + int(res['result']['list'][0][0]) - int(res['result']['list'][1][0])
                    else:
                        print('Bybit downloaded ohlc data is not expected format!')
                        print(res)
                        break
                await asyncio.sleep(0.1)
            if len(ohlcv) > 0:
                mode = 'Updated' if DataWriter.file_exists('bybit', base, quote) else 'Downloaded'
                print(f'{mode} bybit-{symbol} ({base}-{quote}): {len(ohlcv)} records')
                await OHLCConverter.convert_ohlc('bybit', ohlcv, symbol, base, quote)
                await DataWriter.write_data('bybit', symbol, base, quote)
            else:
                print(f'No new data for bybit-{symbol}')


    async def __download_dydx_ohlcv(self, symbol, base, quote, since_ts, till_ts, interval):
        ohlcv = []
        since_ts = since_ts/1000
        async with aiohttp.ClientSession() as session:
            while True:
                # Convert the timestamp to a datetime object
                since_ts_iso = datetime.datetime.utcfromtimestamp(int(since_ts)).isoformat()
                params = {
                    'resolution':interval,
                    'fromISO':since_ts_iso,
                }
                async with session.get(url=self.ohlc_endpoints['dydx']+symbol, params=params) as resp:
                    res = await resp.json()
                    if 'candles' in res:
                        ohlcv.extend(reversed(res['candles']))
                        if len(res['candles']) < 0.5 * self.max_download_per_trial['dydx']:
                            break
                        else:
                            #一番新しいiso日時をtsに変換して10sec加算して再びisoに変換する
                            since_ts = int(isoparse(res['candles'][0]['startedAt']).timestamp()) + 1
                            since_ts_iso = datetime.datetime.utcfromtimestamp(since_ts).isoformat()
                            pass
                    else:
                        print('Dydx downloaded ohlc data is not expected format!')
                        print(res)
                        break
                await asyncio.sleep(0.1)
            if len(ohlcv) > 0:
                mode = 'Updated' if DataWriter.file_exists('dydx', base, quote) else 'Downloaded'
                print(f'{mode} dydx-{symbol} ({base}-{quote}): {len(ohlcv)} records')
                await OHLCConverter.convert_ohlc('dydx', ohlcv, symbol, base, quote)
                await DataWriter.write_data('dydx', symbol, base, quote)
            else:
                print(f'No new data for dydx-{symbol}')


    '''
    since 2023-06-13 11:29:06です, 2023-06-14 12:28:10です
    end  2023-06-15 11:29:55です
    '''
    async def __download_apexpro_ohlcv(self, symbol, base, quote, since_ts, till_ts, interval):
        ohlcv = []
        since_ts = int(since_ts / 1000)
        end_ts = since_ts + (interval * 60 * 1499)
        till_ts = int(till_ts/1000)
        normal_termination = True
        async with aiohttp.ClientSession() as session:
            while True:
                params = {
                    'symbol':symbol,
                    'start':since_ts,
                    'end':end_ts,
                    'interval': interval,
                }
                async with session.get(url=self.ohlc_endpoints['apexpro'], params=params) as resp:
                    res = await resp.json()
                    if len(res['data']) > 0:
                        ohlcv.extend(res['data'][symbol])
                        if len(res['data'][symbol]) < 0.5 * self.max_download_per_trial['apexpro']:
                            break
                        elif int(res['data'][symbol][-1]['t'] / 1000) + 60 >= till_ts:
                            break
                        else:
                            since_ts = int(res['data'][symbol][-1]['t'] / 1000) + 10 #2023-06-14 12:25:10です
                            end_ts = min(since_ts + (interval * 60 * 1499), till_ts) #2023-06-15 11:26:32です, 2023-06-15 13:24:10です
                    else:
                        print('ApeX pro downloaded ohlc data is not expected format for ', symbol)
                        print(res)
                        normal_termination = False
                        break
                await asyncio.sleep(0.01)
            if normal_termination:
                if len(ohlcv) > 0:
                    mode = 'Updated' if DataWriter.file_exists('apexpro', base, quote) else 'Downloaded'
                    print(f'{mode} apexpro-{symbol} ({base}-{quote}): {len(ohlcv)} records')
                    await OHLCConverter.convert_ohlc('apexpro', ohlcv, symbol, base, quote)
                    await DataWriter.write_data('apexpro', symbol, base, quote)
                else:
                    print(f'No new data for apexpro-{symbol}')



    async def __get_tickers(self):
        async with aiohttp.ClientSession() as session:
            for ex in self.exhanges:
                async with session.get(self.ticker_endpoints[ex]) as resp:
                    res = await resp.json()
                    TickerConverter.convert_ticker(ex, res)
                    tickers = TickerData.get_tickers_by_exchange(ex)
                    print('Download Ticker Done for ', ex, ', num tikcers=', len(tickers))





    
    

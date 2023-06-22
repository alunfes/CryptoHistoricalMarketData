import pandas as pd
import asyncio
import os
import pandas as pd
import csv

from OHLCData import OHLCData
from TickerData import TickerData

class DataWriter:
    def __init__(self) -> None:
        pass
    
    @classmethod
    async def write_data(self, exchange, symbol, base, quote):
        #file_name = exchange + '-' + base + '-' + quote + '.parquet'
        file_name = exchange + '-' + base + '-' + quote + '.csv'
        counter = 0
        while True:
            if OHLCData.has_data(exchange, symbol, base, quote):
                break
            await asyncio.sleep(1)
            counter += 1
            if counter > 10:
                print('Data is not found in data writer!')
                print(exchange, symbol, base, quote)
        data = OHLCData.get_data(exchange, symbol, base, quote)
        df = pd.DataFrame(data)
        if exchange == 'okx':
            df = df.iloc[::-1].reset_index(drop=True)
        #df.to_parquet('./app/Data/'+file_name, index=False)
        df.to_csv('./app/Data/'+file_name, index=False)
        OHLCData.delete_data(exchange, symbol, base, quote)

    
    @classmethod
    async def write_ticker_data(self, exchanges):
        with open('./app/all_tickers.csv', 'w', newline='') as csvfile:
            fieldnames = ['ex_name', 'symbol', 'base', 'quote', 'type']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for ex_name in exchanges:
                tickers = TickerData.get_tickers_by_exchange(ex_name)
                for ticker in tickers:
                    writer.writerow({
                        'ex_name': ticker.ex_name, 
                        'symbol': ticker.symbol, 
                        'base': ticker.base, 
                        'quote': ticker.quote, 
                        'type': ticker.type
                    })







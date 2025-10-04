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
    def get_last_timestamp(cls, exchange, base, quote):
        """Get the last timestamp from existing data file, or None if file doesn't exist"""
        file_name = exchange + '-' + base + '-' + quote + '.csv'
        file_path = './app/Data/' + file_name
        
        if not os.path.exists(file_path):
            return None
        
        try:
            df = pd.read_csv(file_path)
            if len(df) > 0 and 'timestamp' in df.columns:
                return int(df['timestamp'].max())
        except Exception as e:
            print(f'Error reading existing file {file_name}: {e}')
        
        return None
    
    @classmethod
    def file_exists(cls, exchange, base, quote):
        """Check if data file exists for given exchange, base, and quote"""
        file_name = exchange + '-' + base + '-' + quote + '.csv'
        file_path = './app/Data/' + file_name
        return os.path.exists(file_path)
    
    @classmethod
    async def write_data(self, exchange, symbol, base, quote):
        #file_name = exchange + '-' + base + '-' + quote + '.parquet'
        file_name = exchange + '-' + base + '-' + quote + '.csv'
        file_path = './app/Data/' + file_name
        counter = 0
        while True:
            if OHLCData.has_data(exchange, symbol, base, quote):
                break
            await asyncio.sleep(1)
            counter += 1
            if counter > 10:
                print('Data is not found in data writer!')
                print(exchange, symbol, base, quote)
                return
        
        data = OHLCData.get_data(exchange, symbol, base, quote)
        new_df = pd.DataFrame(data)
        if exchange == 'okx':
            new_df = new_df.iloc[::-1].reset_index(drop=True)
        
        # Check if file exists and append if it does
        if os.path.exists(file_path):
            try:
                existing_df = pd.read_csv(file_path)
                # Combine existing and new data
                combined_df = pd.concat([existing_df, new_df], ignore_index=True)
                # Remove duplicates based on timestamp, keeping the last occurrence
                combined_df = combined_df.drop_duplicates(subset=['timestamp'], keep='last')
                # Sort by timestamp
                combined_df = combined_df.sort_values('timestamp').reset_index(drop=True)
                combined_df.to_csv(file_path, index=False)
            except Exception as e:
                print(f'Error appending to existing file {file_name}: {e}')
                # Fallback to overwriting
                new_df.to_csv(file_path, index=False)
        else:
            # Create Data directory if it doesn't exist
            os.makedirs('./app/Data', exist_ok=True)
            new_df.to_csv(file_path, index=False)
        
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







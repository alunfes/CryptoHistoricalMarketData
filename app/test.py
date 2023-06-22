from typing import Any


import pandas as pd

class test:
    def __init__(self):
        #df = pd.read_parquet('./app/Data/bybit-1000BONK-USDT.parquet')
        df = pd.read_csv('./app/Data/bybit-BTC-USDT.csv')
        self.__check_ts_diff(df)
        #self.__check_duplication(df)


    def __check_ts_diff(self, df):
        df = df.sort_values("timestamp")
        df['diff'] = df['timestamp'].diff().abs()
        d = list(df['diff'])
        # 差分が60000でない行を探す
        invalid_timestamps = df.loc[df['diff'] != 60000, 'timestamp']
        # invalid_timestampsが空でなければ表示
        if not invalid_timestamps.empty:
            print(invalid_timestamps)
        else:
            print("All timestamps are spaced by 60000.")
        df.to_csv('./app/Data/sorted.csv')


    def __check_duplication(self, df):
        # 重複のチェック
        duplicates = df.duplicated()
        if True in duplicates:
            print('duplicates!')
        # 重複がある場合には最初のデータだけを残す
        df_no_duplicates = df[~duplicates]
        # 結果の表示
        #print(df_no_duplicates['timestamp'])

t = test()
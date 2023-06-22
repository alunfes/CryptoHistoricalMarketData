import datetime



from OHLCData import OHLCData


class OHLCConverter:
    @classmethod
    def initialize(cls):
        cls.__converters = {'okx':cls.__convert_okx_ohlc, 
                            'bybit':cls.__convert_bybit_ohlc,
                            'dydx':cls.__convert_dydx_ohlc,
                            'apexpro':cls.__convert_apexpro_ohlc}
        pass

    @classmethod
    async def convert_ohlc(cls, ex_name, ohlc_json, symbol, base, quote):
        await cls.__converters[ex_name](ohlc_json, symbol, base, quote)

    @classmethod
    async def __convert_okx_ohlc(cls, ohlc_list, symbol, base, quote):
        '''
        [['1686276000000', '26502.6', '26533.2', '26279', '26454.5', '1193839', '11938.39', '314978168.712', '1'], ['1686272400000', '26454.7', '26598', '26438.3', '26502.7', '358361', '3583.61', '95068298.681', '1'], ['1686268800000', '26502.4', '26514.4', '26427.2', '26454.7', '373017', '3730.17', '98707450.164', '1']]
        '''
        timestamps = [int(item[0]) for item in ohlc_list]
        opens = [float(item[1]) for item in ohlc_list]
        highs = [float(item[2]) for item in ohlc_list]
        lows = [float(item[3]) for item in ohlc_list]
        closes = [float(item[4]) for item in ohlc_list]
        OHLCData.add_data('okx', symbol, base, quote, opens, highs, lows, closes, timestamps)

    @classmethod
    async def __convert_bybit_ohlc(cls, ohlc_list, symbol, base, quote):
        '''
        ["1685765160000", "1898.55", "1898.55", "1898.5", "1898.55", "508", "0.26757263"],
            ["1685765100000", "1898", "1898.55", "1898", "1898.55", "1147", "0.60425458"],
            ["1685765040000", "1898.15", "1898.15", "1898", "1898", "5996", "3.15902988"],
            ["1685764980000", "1898.75", "1898.75", "1898.1", "1898.15", "844", "0.4446151"],
            ["16857649200
        '''
        timestamps = [int(item[0]) for item in ohlc_list]
        opens = [float(item[1]) for item in ohlc_list]
        highs = [float(item[2]) for item in ohlc_list]
        lows = [float(item[3]) for item in ohlc_list]
        closes = [float(item[4]) for item in ohlc_list]
        OHLCData.add_data('bybit', symbol, base, quote, opens, highs, lows, closes, timestamps)

    @classmethod
    async def __convert_dydx_ohlc(cls, ohlc_list, symbol, base, quote):
        '''
        [{"startedAt":"2023-06-14T05:00:00.000Z","updatedAt":"2023-06-14T05:18:24.714Z","market":"BTC-USD","resolution":"1HOUR","low":"25973","high":"25989","open":"25981","close":"25981","baseTokenVolume":"134.4184","trades":"381","usdVolume":"3492552.6768","startingOpenInterest":"2521.6992"},{"startedAt":"2023-06-14T04:00:00.000Z","updatedAt":"2023-06-14T04:59:58.918Z","market":"BTC-USD","resolution":"1HOUR","low":"25966","high":"26006","open":"25980","close":"25981","baseTokenVolume":"418.9272","trades":"1386","usdVolume":"10886621.3371","startingOpenInterest":"2518.8522"}
        '''
        timestamps = [int(datetime.datetime.fromisoformat(item['startedAt']).timestamp()) for item in ohlc_list]
        opens = [float(item['open']) for item in ohlc_list]
        highs = [float(item['high']) for item in ohlc_list]
        lows = [float(item['low']) for item in ohlc_list]
        closes = [float(item['close']) for item in ohlc_list]
        OHLCData.add_data('dydx', symbol, base, quote, opens, highs, lows, closes, timestamps)

    @classmethod
    async def __convert_apexpro_ohlc(cls, ohlc_list, symbol, base, quote):
        '''
        [{"s":"BTCUSDC","i":"1","t":1686792300000,"c":"25142.5","h":"25151.5","l":"25137","o":"25150","v":"2.266","tr":"56967.19"},{"s":"BTCUSDC","i":"1","t":1686792360000,"c":"25141.5","h":"25147","l":"25135","o":"25142.5","v":"2.087","tr":"52462.2765"},{"s":"BTCUSDC","i":"1","t":1686792420000,"c":"25122.5","h":"25142","l":"25114","o":"25141.5","v":"2.971","tr":"74668.5635"},{"s":"BTCUSDC","i":"1","t":1686792480000,"c":"25130","h":"25130","l":"25122.5","o":"25122.5","v":"0.384","tr":"9648.2805"},{"s":"BTCUSDC","i":"1","t":1686792540000,"c":"25127.5","h":"25130.5","l":"25126.5","o":"25130","v":"0.586","tr":"14725.031"},{"s":"BTCUSDC","i":"1","t":1686792600000,"c":"25127.5","h":"25127.5","l":"25124.5","o":"25127.5","v":"0.436","tr":"10954.9765"}]},"timeCost":4266657}]
        '''
        timestamps = [int(item['t']) for item in ohlc_list]
        opens = [float(item['o']) for item in ohlc_list]
        highs = [float(item['h']) for item in ohlc_list]
        lows = [float(item['l']) for item in ohlc_list]
        closes = [float(item['c']) for item in ohlc_list]
        OHLCData.add_data('apexpro', symbol, base, quote, opens, highs, lows, closes, timestamps)
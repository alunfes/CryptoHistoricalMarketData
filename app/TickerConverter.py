from TickerData import TickerData

class TickerConverter:
    @classmethod
    def initialize(cls):
        cls.converters = {'okx':cls.__convert_okx_ticker, 
                          'bybit':cls.__convert_bybit_ticker,
                          'dydx':cls.__convert_dydx_ticker,
                          'apexpro':cls.__convert_apexpro_ticker}


    @classmethod
    def convert_ticker(cls, ex_name, ticker_json):
        cls.converters[ex_name](ticker_json)
        

    @classmethod
    def __convert_okx_ticker(cls, ticker_json):
        '''
        {'alias': '', 'baseCcy': '', 'category': '1', 'ctMult': '1', 'ctType': 'inverse', 'ctVal': '100', 'ctValCcy': 'USD', 'expTime': '', 'instFamily': 'BTC-USD', 'instId': 'BTC-USD-SWAP', 'instType': 'SWAP', 'lever': '125', 'listTime': '1611916828000', 'lotSz': '1', ...}
        {'alias': '', 'baseCcy': '', 'category': '1', 'ctMult': '1', 'ctType': 'linear', 'ctVal': '1', 'ctValCcy': 'ANT', 'expTime': '', 'instFamily': 'ANT-USDT', 'instId': 'ANT-USDT-SWAP', 'instType': 'SWAP', 'lever': '50', 'listTime': '1611916828000', 'lotSz': '1', ...}
        '''
        for ticker in ticker_json['data']:
            if ticker['ctType'] == 'linear' and ticker['state']=='live':
                TickerData.add_ticker('okx', ticker['instId'], ticker['ctValCcy'], ticker['settleCcy'], ticker['instType'])

    @classmethod
    def __convert_bybit_ticker(cls, ticker_json):
        '''
        {"retCode":0,"retMsg":"OK","result":{"category":"linear","list":[{"symbol":"10000LADYSUSDT","contractType":"LinearPerpetual","status":"Trading","baseCoin":"10000LADYS","quoteCoin":"USDT","launchTime":"1683802102000","deliveryTime":"0","deliveryFeeRate":"","priceScale":"7","leverageFilter":{"minLeverage":"1","maxLeverage":"25.00","leverageStep":"0.01"},"priceFilter":{"minPrice":"0.0000005","maxPrice":"0.9999990","tickSize":"0.0000005"},"lotSizeFilter":{"maxOrderQty":"24000000","minOrderQty":"100","qtyStep":"100","postOnlyMaxOrderQty":"120000000"},"unifiedMarginTrade":true,"fundingInterval":480,"settleCoin":"USDT"},{"symbol":"10000NFTUSDT","contractType":"LinearPerpetual","status":"Trading","baseCoin":"10000NFT","quoteCoin":"USDT","launchTime":"1643007175000","deliveryTime":"0","deliveryFeeRate":"","priceScale":"6","leverageFilter":{"minLeverage":"1","maxLeverage":"12.50","leverageStep":"0.01"},"priceFilter":{"minPrice":"0.000005","maxPrice":"9.999990","tickSize":"0.000005"},"lotSizeFilter":{"maxOrderQty":"445100","minOrderQty":"10","qtyStep":"10","postOnlyMaxOrderQty":"4451000"},"unifiedMarginTrade":true,"fundingInterval":480,"settleCoin":"USDT"},{"symbol":"1000BONKUSDT","contractType":"LinearPerpetual","status":"Trading","baseCoin":"1000BONK","quoteCoin":"USDT","launchTime":"1672971039000","deliveryTime":"0","deliveryFeeRate":"","priceScale":"6","leverageFilter":{"minLeverage":"1","maxLeverage":"25.00","leverageStep":"0.01"},"priceFilter":{"minPrice":"0.000001","maxPrice":"1.999998","tickSize":"0.000001"},"lotSizeFilter":{"maxOrderQty":"8000000","minOrderQty":"100","qtyStep":"100","postOnlyMaxOrderQty":"40000000"},"unifiedMarginTrade":true,"fundingInterval":480,"settleCoin":"USDT"}
        '''
        for item in ticker_json["result"]["list"]:
            if item["status"] == "Trading":
                TickerData.add_ticker('bybit', item['symbol'], item['baseCoin'], item['quoteCoin'], item['contractType'])

    @classmethod
    def __convert_dydx_ticker(cls, ticker_json):
        '''
        dYdX v4 API response format:
        {"markets":{"BTC-USD":{"ticker":"BTC-USD","status":"ACTIVE","baseAsset":"BTC","quoteAsset":"USD",...}}}
        
        v3 format (for reference):
        {"markets":{"CELO-USD":{"market":"CELO-USD","status":"ONLINE","baseAsset":"CELO","quoteAsset":"USD",...}}}
        '''
        for market, details in ticker_json['markets'].items():
            # v4 uses 'ACTIVE' status instead of 'ONLINE', and 'ticker' instead of 'market'
            status = details.get('status', '')
            if status in ['ONLINE', 'ACTIVE']:  # Support both v3 and v4 formats
                market_name = details.get('ticker', details.get('market', market))
                base_asset = details.get('baseAsset', market.split('-')[0])
                quote_asset = details.get('quoteAsset', market.split('-')[1])
                market_type = details.get('type', 'PERPETUAL')
                TickerData.add_ticker('dydx', market_name, base_asset, quote_asset, market_type)


    @classmethod
    def __convert_apexpro_ticker(cls, ticker_json):
        for ticker in ticker_json['data']["perpetualContract"]:
            if ticker["enableTrade"]:
                TickerData.add_ticker('apexpro', ticker['crossSymbolName'], ticker['underlyingCurrencyId'], ticker['settleCurrencyId'], 'perpetualContract')

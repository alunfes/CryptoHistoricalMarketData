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
        {"markets":{"CELO-USD":{"market":"CELO-USD","status":"ONLINE","baseAsset":"CELO","quoteAsset":"USD","stepSize":"1","tickSize":"0.001","indexPrice":"0.4173","oraclePrice":"0.4167","priceChange24H":"0.000086","nextFundingRate":"0.0000098246","nextFundingAt":"2023-06-14T05:00:00.000Z","minOrderSize":"10","type":"PERPETUAL","initialMarginFraction":"0.2","maintenanceMarginFraction":"0.05","transferMarginFraction":"0.004204","volume24H":"2677351.970000","trades24H":"1849","openInterest":"624888","incrementalInitialMarginFraction":"0.02","incrementalPositionSize":"17700","maxPositionSize":"355000","baselinePositionSize":"35500","assetResolution":"1000000","syntheticAssetId":"0x43454c4f2d36000000000000000000"},"LINK-USD":{"market":"LINK-USD","status":"ONLINE","baseAsset":"LINK","quoteAsset":"USD","stepSize":"0.1","tickSize":"0.001","indexPrice":"5.3934","oraclePrice":"5.3818","priceChange24H":"0.213470","nextFundingRate":"0.0000100141","nextFundingAt":"2023-06-14T05:00:00.000Z","minOrderSize":"1","type":"PERPETUAL","initialMarginFraction":"0.10","maintenanceMarginFraction":"0.05","transferMarginFraction":"0.008147","volume24H":"2699917.002400","trades24H":"3135","openInterest":"316078.7","incrementalInitialMarginFraction":"0.02","incrementalPositionSize":"14000","maxPositionSize":"700000","baselinePositionSize":"70000","assetResolution":"10000000","syntheticAssetId":"0x4c494e4b2d37000000000000000000"},
        '''
        for market, details in ticker_json['markets'].items():
            # Check if the market status is 'ONLINE'
            if details['status'] == 'ONLINE':
                TickerData.add_ticker('dydx', details['market'], details['baseAsset'], details['quoteAsset'], details['type'])


    @classmethod
    def __convert_apexpro_ticker(cls, ticker_json):
        for ticker in ticker_json['data']["perpetualContract"]:
            if ticker["enableTrade"]:
                TickerData.add_ticker('apexpro', ticker['crossSymbolName'], ticker['underlyingCurrencyId'], ticker['settleCurrencyId'], 'perpetualContract')

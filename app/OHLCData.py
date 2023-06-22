import threading

class OHLCData:
    data = {}
    lock = threading.Lock()

    @classmethod
    def initialize(cls):
        with cls.lock:
            cls.data = {}

    @staticmethod
    def add_data(exchange, symbol, base, quote, open_prices, high_prices, low_prices, close_prices, timestamps):
        with OHLCData.lock:
            standardized_data = [
                {
                    'timestamp': timestamp,
                    'open': float(open_price),
                    'high': float(high_price),
                    'low': float(low_price),
                    'close': float(close_price),
                } 
                for open_price, high_price, low_price, close_price, timestamp in zip(open_prices, high_prices, low_prices, close_prices, timestamps)
            ]

            key = (exchange, symbol, base, quote)
            OHLCData.data[key] = standardized_data #[{'timestamp': 1686632400000, 'open': 26056.4, 'high': 26123.0, 'low': 26029.1, 'close': 26077.6}]

    @staticmethod
    def get_data(exchange, symbol, base, quote):
        with OHLCData.lock:
            key = (exchange, symbol, base, quote)
            return OHLCData.data.get(key)

    @staticmethod
    def delete_data(exchange, symbol, base, quote):
        with OHLCData.lock:
            key = (exchange, symbol, base, quote)
            if key in OHLCData.data:
                del OHLCData.data[key]

    @staticmethod
    def get_symbols(exchange):
        with OHLCData.lock:
            return [(symbol, base, quote) for (ex, symbol, base, quote) in OHLCData.data.keys() if ex == exchange]

    @staticmethod
    def has_data(exchange, symbol, base, quote):
        with OHLCData.lock:
            key = (exchange, symbol, base, quote)
            return key in OHLCData.data
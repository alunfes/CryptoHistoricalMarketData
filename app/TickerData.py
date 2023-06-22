import threading

class TickerData:
    _lock = threading.Lock()
    _data = []

    def __init__(self, ex_name, symbol, base, quote, type):
        self.ex_name = ex_name
        self.symbol = symbol
        self.base = base
        self.quote = quote
        self.type = type

    @property
    def ex_name(self):
        return self._ex_name

    @ex_name.setter
    def ex_name(self, value):
        self._ex_name = value

    @property
    def symbol(self):
        return self._symbol

    @symbol.setter
    def symbol(self, value):
        self._symbol = value

    @classmethod
    def initialize(cls):
        with cls._lock:
            cls._data = []

    @classmethod
    def add_ticker(cls, ex_name, symbol, base, quote, type):
        ticker_data = TickerData(ex_name, symbol, base, quote, type)
        with cls._lock:
            cls._data.append(ticker_data)

    @classmethod
    def get_tickers_by_exchange(cls, ex_name):
        with cls._lock:
            return [ticker for ticker in cls._data if ticker.ex_name == ex_name]

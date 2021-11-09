import typing
from stockpicker.modules.exchange.exchange import Exchange
from stockpicker.modules.ticker import Ticker


class NASDAQ(Exchange):
    def get_tickers(self) -> typing.List:
        tickers = []
        with open("../data/nasdaq_screener.csv", 'r') as f:
            for line in f.readlines():
                data = str(line).split(',')
                tickers.append(
                    Ticker(
                        data[0],
                        data[1],
                        "nasdaq",
                        data[9],
                        data[10]
                    ))
        return tickers

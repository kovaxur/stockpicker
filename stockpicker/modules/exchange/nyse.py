from stockpicker.modules.exchange.exchange import Exchange
import requests
import typing


class NYSE(Exchange):
    def get_tickers(self) -> typing.List:
        tickers = []
        response = requests.get("https://api.nasdaq.com/api/screener/stocks?tableonly=true&limit=25&offset=0", timeout=10)
        print(response.status_code)
        json_data = response.json()
        print(json_data)
        return tickers




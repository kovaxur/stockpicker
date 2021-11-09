from yahoo_fin import stock_info as si
import threading
import logging

logger = logging.getLogger("basicLogger")
logger.setLevel(logging.DEBUG)


class YahooFinance(threading.Thread):
    def __init__(self, ticker_queue, task, thread_id):
        super().__init__()
        self.ticker_queue = ticker_queue
        self.task = task
        self.thread_id = thread_id

    def run(self):
        logger.info("Starting thread.")
        if self.task == "roa":
            while not self.ticker_queue.empty():
                ticker = self.ticker_queue.get()
                logger.critical("Starting to get data for ticker: %s. Thread: %s", str(ticker.symbol), str(self.thread_id))
                logger.info("Getting ROA for ticker: %s", ticker.symbol)
                self.add_roa(ticker)
                logger.critical("Finished getting data for ticker: %s. Thread: %s", str(ticker.symbol), str(self.thread_id))
        elif self.task == "pe":
            while not self.ticker_queue.empty():
                ticker = self.ticker_queue.get()
                logger.critical("Starting to get data for ticker: %s. Thread: %s", str(ticker.symbol), str(self.thread_id))
                logger.info("Getting PE for ticker: %s", ticker.symbol)
                self.add_pe(ticker)
                logger.critical("Finished getting data for ticker: %s. Thread: %s", str(ticker.symbol), str(self.thread_id))

    def add_pe(self, ticker):
        try:
            ticker.pe = self.get_pe(ticker.symbol)
        except BaseException as e:
            logger.critical("Critical error found during finding PE: %s", str(e))

    def add_roa(self, ticker):
        try:
            balance_sheet = si.get_balance_sheet(ticker.symbol)
            income_statement = si.get_income_statement(ticker.symbol)
            ticker.roa = self.get_roa(balance_sheet, income_statement) * 100
        except BaseException as e:
            logger.critical("Critical error found during finding ROA: %s", str(e))

    @staticmethod
    def get_pe(symbol):
        data = si.get_quote_table(symbol)
        return data["PE Ratio (TTM)"]

    @staticmethod
    def get_roa(balance_sheet, income_statement):
        current = float(balance_sheet.loc['totalAssets'][0])
        previous = float(balance_sheet.loc['totalAssets'][1])
        av_assets = (current+previous)/2
        net_income = YahooFinance.get_net_income(income_statement)
        return net_income/av_assets

    @staticmethod
    def get_net_income(income_statement):
        net_income = float(income_statement.loc['netIncome'][0])
        return net_income

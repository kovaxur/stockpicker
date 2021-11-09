from stockpicker.modules.exchange.nasdaq import NASDAQ
from stockpicker.modules.yahoofinance import YahooFinance
from stockpicker.modules.queue_monitor import QueueMonitor
import logging
import queue


logger = logging.getLogger("basicLogger")

THREADS = 20


class Picker:
    def find_buys(self):
        self.load_tickers()

    def load_tickers(self):
        nasdaq = NASDAQ()

        # Filter Tickers with proper PE < 20
        logger.critical("Filtering for PE<20")
        tickers = self.filter_tickers_by_pe(5, 20, nasdaq.get_tickers())
        logger.critical("Found number of tickers: %s", str(len(tickers)))
        logger.critical("Filtering in ROA>20")
        tickers = self.filter_tickers_by_min_roa(25, tickers)
        logger.critical("Found number of tickers: %s", str(len(tickers)))

        # Order the list based on ROA -> lower gets less points
        tickers.sort(key=lambda x: x.roa)
        asd = 1
        for ticker in tickers:
            ticker.roa_order = asd
            asd = asd + 1

        # Order the list based on PE -> higher gets less points
        tickers.sort(key=lambda x: x.pe, reverse=True)
        asd = 1
        for ticker in tickers:
            ticker.pe_order = asd
            asd = asd + 1

        for ticker in tickers:
            ticker.points = ticker.roa_order + ticker.pe_order

        tickers.sort(key=lambda x: x.points, reverse=True)
        for ticker in tickers:
            logger.critical("Symbol: %s, Points: %s, ROA: %s(%s), PE: %s(%s)",
                            str(ticker.symbol), str(ticker.points), str(ticker.roa),
                            str(ticker.roa_order), str(ticker.pe), str(ticker.pe_order))

    def filter_tickers_by_min_roa(self, min_roa, tickers):
        ticker_queue = queue.Queue()
        qm = QueueMonitor(ticker_queue, "roa")
        qm.start()

        for ticker in tickers:
            ticker_queue.put(ticker)

        worker_threads = []
        for i in range(0, THREADS):
            logger.critical("Starting thread %s", str(i))
            th = YahooFinance(ticker_queue, "roa")
            th.start()
            worker_threads.append(th)

        for i in worker_threads:
            i.join()
        qm.stop = True
        qm.join()

        # Eliminating tickers with ROA lower than 20%
        interesting_tickers = []
        for ticker in tickers:
            if ticker.roa is not None and ticker.roa > min_roa:
                logger.info("Found interesting ticker: %s (%s)", ticker.symbol, ticker.name)
                interesting_tickers.append(ticker)
            else:
                logger.info("Ticker checked, but it's not interesting: %s (%s)", ticker.symbol, ticker.name)
        return interesting_tickers

    def filter_tickers_by_pe(self, min_pe, max_pe, tickers):
        ticker_queue = queue.Queue()
        qm = QueueMonitor(ticker_queue, "pe")
        qm.start()

        for ticker in tickers:
            ticker_queue.put(ticker)

        worker_threads = []
        for i in range(0, THREADS):
            logger.critical("Starting thread %s", str(i))
            th = YahooFinance(ticker_queue, "pe")
            th.start()
            worker_threads.append(th)

        for i in worker_threads:
            i.join()
        qm.stop = True
        qm.join()

        # Eliminating tickers with PE higher than max_pe
        interesting_tickers = []
        for ticker in tickers:
            if ticker.pe is not None and max_pe > ticker.pe > min_pe:
                logger.critical("Found interesting ticker with proper PE: %s (%s)", ticker.symbol, ticker.pe)
                interesting_tickers.append(ticker)
            else:
                logger.info("Ticker checked, but it's not interesting: %s (%s)", ticker.symbol, ticker.name)
        return interesting_tickers




import threading
import time
import logging

logger = logging.getLogger("basicLogger")


class QueueMonitor(threading.Thread):
    def __init__(self, queue, name):
        super().__init__()
        self.queue = queue
        self.stop = False
        self.name = name

    def run(self):
        while not self.stop:
            logger.critical("Number of tickers waiting for task: %s: %s", self.name, str(self.queue.qsize()))
            time.sleep(5)


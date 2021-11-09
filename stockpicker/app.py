from stockpicker.modules.picker import Picker
import logging

logger = logging.getLogger("basicLogger")
logger.setLevel(logging.DEBUG)

class StockPicker:
    def run(self):
        picker = Picker()
        picker.find_buys()


if __name__ == "__main__":
    sp = StockPicker()
    sp.run()

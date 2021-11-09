

class Ticker:
    def __init__(self, symbol, name, exchange, sector, industry):
        self.symbol = symbol
        self.name = name
        self.exchange: exchange
        self.sector = sector
        self.industry = industry
        self.roa = None
        self.pe = None
        self.roa_order = None
        self.pe_order = None
        self.score = None

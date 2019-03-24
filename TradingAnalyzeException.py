class TradingAnalyzeException(Exception):

    def __init__(self, message, log_path, is_first_currency_closes_empty=False):
        self.message = message
        self.log_path = log_path
        self.is_first_currency_closes_empty = is_first_currency_closes_empty

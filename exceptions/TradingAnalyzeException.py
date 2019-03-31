class TradingAnalyzeException(Exception):

    def __init__(self, message, log_path, is_first_currency_closes_empty=False, is_first_currency_closes_small_size=False):
        self.message = message
        self.log_path = log_path
        self.is_first_currency_closes_empty = is_first_currency_closes_empty
        self.is_first_currency_closes_small_size = is_first_currency_closes_small_size

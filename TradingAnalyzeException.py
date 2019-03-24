class TradingAnalyzeException(Exception):

    def __init__(self, message, log_path):
        self.message = message
        self.log_path = log_path

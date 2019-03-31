class Config:
    LOGGING_PATH = 'C:/ArbitrageTrading'
    COINTEGRATION_LOG_PATH = 'C:/ArbitrageTrading/CointegrationInfos'
    COINTERGRATION_INFO_JSON_FILENAME = 'log_cointegration_info.json'
    COINTEGRATION_INFO_TXT_FILENAME = 'log_cointegration_info.txt'
    SERIES_DIFFERENCE_PERCENT_THRESHOLD = 0.2


class BinanceConfig(Config):
    API_KEY = 'F95r3yBjC0q5vblzgqo8WUqwOsfqNBNbSoHTRg23bjPmoReKLBsMjId4C5s0dgHT'
    API_SECRET = 'whYmJzFzObWvkfI38pGNFyTdTeejxr8dimpS5sHxQXBHXx04RtjIV9fX8sc8mPqf'
    TICKERS_GETTER_INTERVAL_15M = '15m'
    TICKERS_GETTER_START_DATE_15M = '2019-02-25 18:30 UTC'
    TICKERS_GETTER_END_DATE_15M = '2019-03-25 18:30 UTC'

    TICKERS_GETTER_INTERVAL_5M = '5m'
    TICKERS_GETTER_START_DATE_5M = '2019-03-20 15:00 UTC'
    TICKERS_GETTER_END_DATE_5M = '2019-03-25 18:30 UTC'

    TICKERS_GETTER_INTERVAL_1M = '1m'
    TICKERS_GETTER_START_DATE_1M = '2019-03-29 00:00 UTC'
    TICKERS_GETTER_END_DATE_1M = '2019-03-30 12:30 UTC'
    COMMISSION = 0.0005

    TICKERS_GETTER_INTERVAL_1H = '1h'
    TICKERS_GETTER_START_DATE_1H = '2018-11-28 05:00 UTC'
    TICKERS_GETTER_END_DATE_1H = '2019-03-28 05:00 UTC'

    MAJOR_CURRENCIES = ['BTC', 'ETH', 'USDT', 'USDC']

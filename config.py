class Config:

    LOGGING_PATH = 'C:/ArbitrageTrading'
    COINTEGRATION_LOG_PATH = 'C:/ArbitrageTrading/CointegrationInfos'

    SERIES_DIFFERENCE_PERCENT_THRESHOLD = 0.2



class BinanceConfig(Config):

    API_KEY = 'F95r3yBjC0q5vblzgqo8WUqwOsfqNBNbSoHTRg23bjPmoReKLBsMjId4C5s0dgHT'
    API_SECRET = 'whYmJzFzObWvkfI38pGNFyTdTeejxr8dimpS5sHxQXBHXx04RtjIV9fX8sc8mPqf'
    TICKERS_GETTER_INTERVAL = '15m'
    TICKERS_GETTER_START_DATE = '2019-02-23 15:00 UTC'
    TICKERS_GETTER_END_DATE = '2019-03-23 15:00 UTC'

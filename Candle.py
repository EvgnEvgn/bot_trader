class Candle:
    def __init__(self, args):
        self.openTime = args[0]
        self.open = args[1]
        self.high = args[2]
        self.low = args[3]
        self.close = args[4]
        self.volume = args[5]
        self.closeTime = args[6]
        self.quoteAssetVolume = args[7]
        self.numberOfTrades = args[8]
        self.takerBuyBaseAssetVolume = args[9]
        self.takerBuyQuoteAssetVolume = args[10]
        self.ignore = args[11]

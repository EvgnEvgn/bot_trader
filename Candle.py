class Candle:
    # [
    #  1499040000000, // Open time
    # "0.01634790", // Open
    # "0.80000000", // High
    # "0.01575800", // Low
    # "0.01577100", // Close
    # "148976.11427815", // Volume
    # 1499644799999, // Close time
    # "2434.19055334", // Quote asset volume
    # 308, // Number of trades
    # "1756.87402397", // Taker
    # buy
    # base
    # asset
    # volume
    # "28.46694368", // Taker
    # buy
    # quote
    # asset
    # volume
    # "17928899.62484339" // Ignore.
    # ]
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

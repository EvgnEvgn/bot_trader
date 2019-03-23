from binance.client import Client
from datetime import datetime, timezone
from Candle import Candle
from binance.websockets import BinanceSocketManager

api_key = 'F95r3yBjC0q5vblzgqo8WUqwOsfqNBNbSoHTRg23bjPmoReKLBsMjId4C5s0dgHT'
api_secret = 'whYmJzFzObWvkfI38pGNFyTdTeejxr8dimpS5sHxQXBHXx04RtjIV9fX8sc8mPqf'

client = Client(api_key, api_secret)

# get all symbol prices
# prices = client.get_all_tickers()
# print(prices)


ticker = 'XRPBTC'
interval = '5m'
start_date = '2019-03-23 8:00 UTC'
end_date = '2019-03-23 11:00 UTC'

candles = []
result = client.get_historical_klines(ticker, interval, start_date, end_date)
for candle in result:
    candles.append(Candle(candle))

bla = 0


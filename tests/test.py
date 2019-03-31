from config import BinanceConfig
import datetime
from objects.BinanceClientSingleton import BinanceClientSingleton

print(datetime.datetime.now())
client = BinanceClientSingleton().get_client()
result = client.get_historical_klines('RVNBTC', BinanceConfig.TICKERS_GETTER_INTERVAL_1M,
                             '2018-10-02 18:30 UTC',
                             '2019-03-31 18:30 UTC')

client1 = BinanceClientSingleton().get_client()

print(client)
print(client1)
print(datetime.datetime.now())
blabla = 0

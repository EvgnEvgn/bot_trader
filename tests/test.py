import datetime
from objects.CurrencyPair import CurrencyPair
from decorators.cointegration_analyzer_decorators import logarithm_currency_pair
print(datetime.datetime.now())
# client = BinanceClientSingleton().get_client()
# result = client.get_historical_klines('RVNBTC', BinanceConfig.TICKERS_GETTER_INTERVAL_1M,
#                              '2018-10-02 18:30 UTC',
#                              '2019-03-31 18:30 UTC')
#
# client1 = BinanceClientSingleton().get_client()
#
# print(client)
# print(client1)
# print(datetime.datetime.now())
# blabla = 0


@logarithm_currency_pair
def do_smth(arg1, arg2) -> CurrencyPair:
    currency_pair = CurrencyPair()
    currency_pair.first_currency_closes = [0.04, 0.05, 0.11, 0.22]
    currency_pair.second_currency_closes = [0.02, 0.15, 0.1444, 0.122]

    return currency_pair


cp = do_smth(1, 2)

print(cp.first_currency_closes)
print(cp.second_currency_closes)
from objects.BinanceClientSingleton import BinanceClientSingleton as BinanceClient
from config import BinanceConfig
from objects.CurrencyPair import CurrencyPair
from cointegration_analyzer.currency_pair_cointegration_analyzer import set_currency_pair_info
from scipy.stats.stats import pearsonr
import numpy


def check_correlation(currency_pair: CurrencyPair):

    if currency_pair.first_currency_closes.empty or currency_pair.second_currency_closes.empty:
        print("No data.")
    else:
        correlation = pearsonr(currency_pair.first_currency_closes, currency_pair.second_currency_closes)
        print(correlation)
        print(numpy.corrcoef(currency_pair.first_currency_closes, currency_pair.second_currency_closes))


currency_pair = CurrencyPair()
currency_pair.first_currency_name = 'RVNBTC'
currency_pair.second_currency_name = 'XRPBTC'

client = BinanceClient.get_instance().get_client()

currency_pair = set_currency_pair_info(currency_pair,
                                       BinanceConfig.TICKERS_GETTER_INTERVAL_1H,
                                       BinanceConfig.TICKERS_GETTER_START_DATE_1H,
                                       BinanceConfig.TICKERS_GETTER_END_DATE_1H,
                                       client)

# currency_pair.first_currency_closes = numpy.log(currency_pair.first_currency_closes)
# currency_pair.second_currency_closes = numpy.log(currency_pair.second_currency_closes)

check_correlation(currency_pair)

currency_pair = set_currency_pair_info(currency_pair,
                                       BinanceConfig.TICKERS_GETTER_INTERVAL_15M,
                                       BinanceConfig.TICKERS_GETTER_START_DATE_15M,
                                       BinanceConfig.TICKERS_GETTER_END_DATE_15M,
                                       client)
# currency_pair.first_currency_closes = numpy.log(currency_pair.first_currency_closes)
# currency_pair.second_currency_closes = numpy.log(currency_pair.second_currency_closes)
check_correlation(currency_pair)

currency_pair = set_currency_pair_info(currency_pair,
                                       BinanceConfig.TICKERS_GETTER_INTERVAL_5M,
                                       BinanceConfig.TICKERS_GETTER_START_DATE_5M,
                                       BinanceConfig.TICKERS_GETTER_END_DATE_5M,
                                       client)
# currency_pair.first_currency_closes = numpy.log(currency_pair.first_currency_closes)
# currency_pair.second_currency_closes = numpy.log(currency_pair.second_currency_closes)
check_correlation(currency_pair)

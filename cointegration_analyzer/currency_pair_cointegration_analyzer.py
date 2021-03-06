from objects.BinanceClientSingleton import BinanceClientSingleton as BinanceClient
from objects.Candle import Candle
from trading_algorithms import ArbitrageTradingAlgorithm as ATA
import pandas as pd
from objects.CurrencyPair import CurrencyPair
from config import Config, BinanceConfig
import os
from exceptions.TradingAnalyzeException import TradingAnalyzeException
from Loggers.logger import Logger
import dateparser as dp
from helpers.file_helper import is_file_exists_in_dir
from decorators.cointegration_analyzer_decorators import logarithm_currency_pair


def get_major_currency_path(major_currency):
    start_date = dp.parse(BinanceConfig.TICKERS_GETTER_START_DATE_15M).strftime("%d-%m-%Y")

    end_date = dp.parse(BinanceConfig.TICKERS_GETTER_END_DATE_15M).strftime("%d-%m-%Y")
    major_currency_path = '{0}/{1}_{2}_{3}_{4}'.format(Config.LOGGING_PATH,
                                                       major_currency,
                                                       BinanceConfig.TICKERS_GETTER_INTERVAL_15M,
                                                       start_date,
                                                       end_date)

    return major_currency_path


@logarithm_currency_pair
def set_currency_pair_info(currency_pair, interval, s_date, e_date,
                           current_currency_pair_path=None) -> CurrencyPair:
    client = BinanceClient().get_client()

    first_currency_candles = []
    second_currency_candles = []

    first_currency_closes = []
    second_currency_closes = []
    Logger.log_info(current_currency_pair_path,
                    "Получаем с бинанса данные о свечах пар {0} и {1}...".format(currency_pair.first_currency_name,
                                                                                 currency_pair.second_currency_name))
    result1 = client.get_historical_klines(currency_pair.first_currency_name, interval, s_date, e_date)
    result2 = client.get_historical_klines(currency_pair.second_currency_name, interval, s_date, e_date)

    Logger.log_info(current_currency_pair_path, "Данные пришли.")
    result1_len = len(result1)
    result2_len = len(result2)

    Logger.log_info(current_currency_pair_path,
                    "Кол-во данных по {0}: {1}.".format(currency_pair.first_currency_name, result1_len))
    Logger.log_info(current_currency_pair_path,
                    "Кол-во данных по {0}: {1}.".format(currency_pair.second_currency_name, result2_len))

    if result1_len == 0 or result2_len == 0:
        raise TradingAnalyzeException("Данных нет.", current_currency_pair_path,
                                      is_first_currency_closes_empty=result1_len == 0)

    diff = result1_len - result2_len
    diff_percent = 0.0
    is_first_currency_more = False

    if diff > 0:
        diff_percent = abs(diff) / result1_len
        is_first_currency_more = True
    else:
        diff_percent = abs(diff) / result2_len

    if diff_percent > Config.SERIES_DIFFERENCE_PERCENT_THRESHOLD:
        raise TradingAnalyzeException("Данные по валютам слишком отличаются в размерах.", current_currency_pair_path,
                                      is_first_currency_closes_small_size=not is_first_currency_more)

    elif is_first_currency_more:
        result1 = result1[abs(diff):]
    else:
        result2 = result2[abs(diff):]

    for i in range(0, len(result1) - 1):
        first_currency_candle = Candle(result1[i])
        second_currency_candle = Candle(result2[i])

        first_currency_candles.append(first_currency_candle)
        second_currency_candles.append(second_currency_candle)

        first_currency_closes.append(first_currency_candle.close)
        second_currency_closes.append(second_currency_candle.close)

    currency_pair.first_currency_closes = pd.Series(first_currency_closes)
    currency_pair.second_currency_closes = pd.Series(second_currency_closes)

    return currency_pair


def get_grouped_tickers(tickers, major_currencies):
    grouped_tickers = {}

    for major_currency in major_currencies:

        current_tickers = []
        for ticker in tickers:
            if ticker['symbol'].rfind(major_currency) > 0:
                current_tickers.append(ticker['symbol'])

        grouped_tickers.update({major_currency: current_tickers})

    return grouped_tickers


def set_quote_volume_to_currency_pair(currency_pair: CurrencyPair):
    # TODO понять разницу между quoteVolume и просто volume
    client = BinanceClient().get_client()

    quote_volume_result = client.get_ticker(symbol=currency_pair.first_currency_name).get('quoteVolume')

    if quote_volume_result:
        currency_pair.set_first_currency_volume(quote_volume_result)

    quote_volume_result = client.get_ticker(symbol=currency_pair.second_currency_name).get('quoteVolume')

    if quote_volume_result:
        currency_pair.set_second_currency_volume(quote_volume_result)


def run():
    client = BinanceClient().get_client()

    tickers = client.get_all_tickers()

    grouped_tickers = get_grouped_tickers(tickers, BinanceConfig.MAJOR_CURRENCIES)

    for major_currency, gp in grouped_tickers.items():

        major_currency_path = get_major_currency_path(major_currency)
        print("Мажорная валюта: {0}.".format(major_currency))

        if not os.path.isdir(major_currency_path):
            os.mkdir(major_currency_path)

        current_grouped_tickers = gp
        current_tickers_len = len(current_grouped_tickers)

        for i in range(0, current_tickers_len - 1):
            first_currency = current_grouped_tickers.pop()

            if len(current_grouped_tickers) != 0:
                for second_currency in current_grouped_tickers:
                    try:
                        currency_pair = CurrencyPair()
                        currency_pair.first_currency_name = first_currency
                        currency_pair.second_currency_name = second_currency

                        current_currency_pair_path = '{0}/{1}_{2}'.format(major_currency_path,
                                                                          currency_pair.first_currency_name,
                                                                          currency_pair.second_currency_name)

                        if not os.path.isdir(current_currency_pair_path):
                            os.mkdir(current_currency_pair_path)

                        else:
                            if is_file_exists_in_dir(current_currency_pair_path, Config.RESIDUES_RESULT_FILENAME):
                                continue

                        currency_pair = set_currency_pair_info(currency_pair,
                                                               BinanceConfig.TICKERS_GETTER_INTERVAL_15M,
                                                               BinanceConfig.TICKERS_GETTER_START_DATE_15M,
                                                               BinanceConfig.TICKERS_GETTER_END_DATE_15M,
                                                               major_currency_path)

                        result_cointegration_currency_pair = ATA.run(currency_pair, current_currency_pair_path)

                        # Установим объем торгов если пары коинтегрированны
                        if result_cointegration_currency_pair.is_stationarity:

                            set_quote_volume_to_currency_pair(result_cointegration_currency_pair)

                            Logger.log_cointegration_info(result_cointegration_currency_pair, major_currency_path)

                    except TradingAnalyzeException as ex:
                        Logger.log_info(ex.log_path, ex.message)
                        if ex.is_first_currency_closes_empty or ex.is_first_currency_closes_small_size:
                            break
                    except Exception as ex:
                        print('Неопознанная ошибка! ')
                        print(ex)


# run()
